import './style.css'
import { VideoHandler } from './videoHandler';


const API_URL = 'http://localhost:5000'

let video = document.getElementById('input-video') as HTMLMediaElement;
let videoSource = document.createElement('source') as HTMLSourceElement;

const fileInput = document.getElementById('file-input');

const videoHandler = new VideoHandler(document.querySelector('.content-container'));

fileInput?.addEventListener('change', async (event) => {
  // if (video.hasChildNodes()) {
  //   // TODO: Выделить в отдельную функцию/класс инстанцирование видео
  //   video.remove();
  //   video.removeChild(videoSource);
  //   let videoContainer = document.querySelector('.video-container');
  //   const newVideo = document.createElement('video');

  //   newVideo.setAttribute('controls', 'true');
  //   newVideo.id = 'input-video';
  //   newVideo.width = 320;
    
  //   videoContainer?.appendChild(newVideo);
  //   video = newVideo;
  // }
  // event.preventDefault();


  // video.addEventListener('timeupdate', () => {
  //   if (video.currentTime > 2) {
  //     console.log(video.currentTime);
  //   }
  // })

  const formData = new FormData();
  let file = (event.target as HTMLInputElement).files![0];  

  if (file) {
    formData.append('file', file);
    
    // const src = URL.createObjectURL(file);
    // videoSource.setAttribute('src', src)
    // video?.appendChild(videoSource);
    
    videoHandler.loadFile(file);
  }

  if (formData) {
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

