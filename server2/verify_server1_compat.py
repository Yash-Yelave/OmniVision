import asyncio
import httpx

async def test_rest():
    url = "http://localhost:8001/internal/full-pipeline"
    print(f"Testing {url}...")
    
    # We just need a dummy image
    try:
        with open("test_image.jpg", "rb") as f:
            file_bytes = f.read()
    except FileNotFoundError:
        print("test_image.jpg not found, creating a dummy file...")
        with open("test_image.jpg", "wb") as f:
            f.write(b"dummy image data")
        file_bytes = b"dummy image data"
            
    files = {'file': ("test_image.jpg", file_bytes, "image/jpeg")}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, files=files, timeout=60.0)
            print(f"Status Code: {response.status_code}")
            try:
                print(f"Response: {response.json()}")
            except Exception:
                print(f"Text Response: {response.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_rest())
