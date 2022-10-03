export class VideoHandler {

  private readonly FRAMERATE: number = 25;
  private readonly WIDTH: number = 600;
  private readonly HEIGHT: number = 400;
  private X_SCALE: number = 1;
  private Y_SCALE: number = 1;

  private _contentContainer: HTMLDivElement;

  private video: HTMLVideoElement;
  private _videoCurrentTime: number = 0;
  private _videoDuration: number = 0;

  public originalVideoWidth: number = 0;
  public originalVideoHeight: number = 0;

  private canvas: HTMLCanvasElement;
  private faceData: FaceData[] = [];

  constructor(parent: Element | null) {
    this._contentContainer = document.createElement('div');
    this._contentContainer.setAttribute('class', 'video-handler-content');

    this.video = document.createElement('video');
    this.video.id = 'input-video';
    this.video.controls = true;
    this.video.width = this.WIDTH;
    this.video.height = this.HEIGHT;

    this.canvas = document.createElement('canvas');
    this.canvas.id = 'input-canvas';
    this.canvas.width = this.WIDTH;
    this.canvas.height = this.HEIGHT;


    this._contentContainer.appendChild(this.video);
    this._contentContainer.appendChild(this.canvas);

    if (parent) parent.appendChild(this._contentContainer);

    // handling play video button
    this.video.addEventListener('play', () => {
      if (this.faceData.length != 0) {
        this.playHandler();
      }
      else {
        console.error('faceData empty');
      }
    })

    // handling video timeline
    this.video.addEventListener('timeupdate', () => {
      this._videoCurrentTime = this.video.currentTime;
    })
  }

  loadFile(file: File) {
    if (this.video.hasChildNodes()) {
      this.video.remove();
      this.faceData = [];

      this.video = document.createElement('video');
      this.video.id = 'input-video';
      this.video.controls = true;
      this.video.width = this.WIDTH;
      this.video.height = this.HEIGHT;

      this._contentContainer.prepend(this.video);
      this.video.addEventListener('play', () => {
        if (this.faceData.length != 0) {
          this.playHandler();
        }
        else {
          console.error('faceData empty');
        }
      })
    }
    // Get original size 
    this.video.addEventListener('loadedmetadata', () => {
      this.originalVideoWidth = this.video.videoWidth;
      this.originalVideoHeight = this.video.videoHeight;
      this._videoDuration = this.video.duration;
      this.X_SCALE = this.WIDTH / this.originalVideoWidth;
      this.Y_SCALE = this.HEIGHT / this.originalVideoHeight;
    })

    const objectURL = URL.createObjectURL(file);
    console.log(file);
    const videoSource = document.createElement('source') as HTMLSourceElement;
    videoSource.setAttribute('src', objectURL)

    this.video.appendChild(videoSource);
  }

  loadData(data: FaceData[]) {
    this.faceData = data;
  }

  drawDetection(context: CanvasRenderingContext2D, iter: number) {
    const currentData = this.faceData[iter];
    console.log(currentData);

    if (currentData) {

      const x1 = currentData[0];
      const y1 = currentData[1];
      const x2 = currentData[2];
      const y2 = currentData[3];

      const x = x1 * this.X_SCALE;
      const y = y1 * this.Y_SCALE;
      const w = (x2 - x1) * this.X_SCALE;
      const h = (y2 - y1) * this.Y_SCALE;

      context.strokeRect(x, y, w, h);
    }
  }

  private playHandler() {
    const ctx = this.canvas.getContext('2d');

    let currentFrame = 0; 
    const loop = () => {
      if (!this.video.paused && !this.video.ended) {
        this._videoCurrentTime = this.video.currentTime;
        currentFrame = this._videoCurrentTime * this.FRAMERATE;

        ctx!.drawImage(this.video, 0, 0, this.WIDTH, this.HEIGHT);

        this.drawDetection(ctx!, Math.round(currentFrame));

        setTimeout(loop, 1000 / this.FRAMERATE); // drawing at 25fps
      }
    };

    loop();
  }
}

type FaceData = {
  0: number;
  1: number;
  2: number;
  3: number;
  4: number;
}