import './style.css'
import { VideoHandler } from './videoHandler';

// TODO: Вынести в отдельный namespace api
const API_URL = 'http://localhost:5000'

const fileInput = document.getElementById('file-input');

const detectorTypeInput: HTMLInputElement = document.querySelector('#detector-type')!;

const videoHandler = new VideoHandler(document.querySelector('.content-container'));


fileInput?.addEventListener('change', async (event) => {

  const formData = new FormData();

  const file = (event.target as HTMLInputElement).files![0]; 
  const detectorType = detectorTypeInput.value;

  if (file) {
    formData.append('file', file);
    videoHandler.loadFile(file);
  }

  formData.append('detector_type', detectorType);

  if (formData) {
    // TODO: Вынести в отдельный namespace api
    try {
      const response = await fetch(`${API_URL}/upload`, {method:'POST', body:formData});
      if (response.ok) {
        const data = await response.json();
        videoHandler.loadDetectionData(data['data']);
      }
    } catch(e) {
      console.log(e);
    }
    
  }
})

