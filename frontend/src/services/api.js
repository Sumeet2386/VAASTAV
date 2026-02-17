const BASE_URL = "http://127.0.0.1:8000/api";

async function postFile(endpoint, file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/${endpoint}`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error(await res.text());
  }

  return res.json();
}

export const verifyImage = (file) =>
  postFile("image", file);

export const verifyVideo = (file) =>
  postFile("video", file);

export const verifyCertificate = (file) =>
  postFile("certificate", file);
