import './style.css'
import { VideoHandler } from './videoHandler';

// TODO: Вынести в отдельный namespace api
const API_URL = 'http://localhost:5000'

const fileInput = document.getElementById('file-input');

const videoHandler = new VideoHandler(document.querySelector('.content-container'));

fileInput?.addEventListener('change', async (event) => {

  const formData = new FormData();
  let file = (event.target as HTMLInputElement).files![0];  

  if (file) {
    formData.append('file', file);
    
    videoHandler.loadFile(file);
  }

  if (formData) {
    // TODO: Вынести в отдельный namespace api
    try {
      const response = await fetch(`${API_URL}/upload`, {method:'POST', body:formData});
      if (response.ok) {
        const data = await response.json();
        videoHandler.loadData(data['data']);
      }
    } catch(e) {
      console.log(e);
    }
    
  }
})

