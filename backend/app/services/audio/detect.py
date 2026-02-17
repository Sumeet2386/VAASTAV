import librosa
import numpy as np

# -------------------------------------------------
# FEATURE EXTRACTION
# -------------------------------------------------

def extract_features(audio_path):
    try:
        y, sr = librosa.load(audio_path, sr=None)
    except Exception as e:
        return {"error": str(e)}

    features = {}

    # 1️⃣ Pitch Analysis (pYIN)
    try:
        f0, _, _ = librosa.pyin(
            y,
            fmin=librosa.note_to_hz('C2'),
            fmax=librosa.note_to_hz('C7')
        )

        if f0 is not None and np.any(~np.isnan(f0)):
            features["pitch_std"] = float(np.nanstd(f0))
            features["pitch_range"] = float(np.nanmax(f0) - np.nanmin(f0))
        else:
            features["pitch_std"] = 0.0
            features["pitch_range"] = 0.0

    except:
        features["pitch_std"] = 0.0
        features["pitch_range"] = 0.0

    # 2️⃣ Spectral Flatness
    flatness = librosa.feature.spectral_flatness(y=y)
    features["spectral_flatness_mean"] = float(np.mean(flatness))

    # 3️⃣ RMS Energy
    rms = librosa.feature.rms(y=y)[0]
    features["energy_std"] = float(np.std(rms))
    features["energy_range"] = float(np.max(rms) - np.min(rms))

    # 4️⃣ Silence Analysis
    non_silent = librosa.effects.split(y, top_db=20)

    if len(non_silent) > 1:
        silence_durations = []
        for i in range(len(non_silent) - 1):
            silence_start = non_silent[i][1]
            silence_end = non_silent[i+1][0]
            duration = (silence_end - silence_start) / sr
            silence_durations.append(duration)

        features["pause_std"] = float(np.std(silence_durations)) if silence_durations else 0.0
        features["pause_count"] = len(silence_durations)
    else:
        features["pause_std"] = 0.0
        features["pause_count"] = 0

    # 5️⃣ Zero Crossing Rate
    zcr = librosa.feature.zero_crossing_rate(y)
    features["zcr_mean"] = float(np.mean(zcr))

    # 6️⃣ MFCC Variance
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_var = np.var(mfcc[1:], axis=1)
    features["mfcc_mean_var"] = float(np.mean(mfcc_var))

    # 7️⃣ Digital Silence
    features["min_amplitude"] = float(np.min(np.abs(y)))

    return features


# -------------------------------------------------
# AUTHENTICITY SCORING
# -------------------------------------------------

def calculate_authenticity_score(features):
    score = 0
    reasons = []

    # Pitch stability
    if features["pitch_std"] < 30:
        score += 30
        reasons.append("Pitch variation is unusually stable.")

    # Spectral flatness
    if features["spectral_flatness_mean"] < 0.02:
        score += 15
        reasons.append("Spectrum is highly tonal and clean.")

    # Energy consistency
    if features["energy_std"] < 0.05:
        score += 20
        reasons.append("Volume consistency suggests normalization.")

    # Pause uniformity
    if features["pause_count"] > 1 and features["pause_std"] < 0.15:
        score += 15
        reasons.append("Pause durations are highly uniform.")

    # Digital silence
    if features["min_amplitude"] < 1e-4:
        score += 10
        reasons.append("Contains near-perfect digital silence.")

    # MFCC smoothness
    if features["mfcc_mean_var"] < 500:
        score += 20
        reasons.append("Voice timbre appears overly smooth.")

    score = max(0, min(100, score))

    verdict = "Likely AI Generated" if score > 50 else "Likely Human"

    return {
        "verdict": verdict,
        "confidence": score,
        "reasons": reasons,
        "features": features
    }


# -------------------------------------------------
# MAIN ENTRY FUNCTION
# -------------------------------------------------

def verify_audio(file_path):
    features = extract_features(file_path)

    if "error" in features:
        return {
            "verdict": "Audio Processing Error",
            "confidence": 0,
            "reasons": [features["error"]],
            "features": {}
        }

    return calculate_authenticity_score(features)
