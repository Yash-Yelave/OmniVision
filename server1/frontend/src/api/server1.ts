export const BASE_URL = 'http://192.168.0.140:8000';

export const analyzeImage = async (imageFile: File | Blob) => {
  const formData = new FormData();
  formData.append('file', imageFile, 'capture.jpg');

  const response = await fetch(`${BASE_URL}/api/analyze`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Analyze API error: ${response.statusText}`);
  }

  return response.json();
};

export const sendGesture = async (frames: any[]) => {
  const response = await fetch(`${BASE_URL}/api/gesture`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ frames }),
  });

  if (!response.ok) {
    throw new Error(`Gesture API error: ${response.statusText}`);
  }

  return response.json();
};
