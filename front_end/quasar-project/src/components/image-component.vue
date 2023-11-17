<template>
  <div id="img_data">
    <q-uploader
      ref="uploader"
      id="uploader"
      url="/upload"
      no-thumbnails
      square
      name="file"
      @added="onFileAdded"
    />
  </div>
  <div id="map" class="map"></div>
</template>
<script>
import Map from 'ol/Map';
import View from 'ol/View';
import {Projection, transform} from "ol/proj";
import ImageLayer from "ol/layer/Image";
import Static from 'ol/source/ImageStatic';
import {getCenter} from "ol/extent";
import * as buffer from "buffer";
import {ref} from "vue";
export default {
  name: "image-component",
  data(){
    return{
      file_name:"",
    }
  },
  computed: {
    buffer() {
      return buffer
    }
  },
  setup() {
    return {
      model: ref(null)

    }
  },
  mounted() {
    this.initMap();
  },
  methods: {
    initMap: function () {
      const extent = [100, 100, 500, 480];
      const projection = new Projection({
        code: 'xkcd-image',
        units: 'pixels',
        extent: extent,
      });
      const map = new Map({
        layers: [
          new ImageLayer({
            source: new Static({
              url: 'logo.png',
              projection: projection,
              imageExtent: extent,
            }),
          }),
        ],
        target: 'map',
        view: new View({
          projection: projection,
          center: getCenter(extent),
          zoom: 2,
          maxZoom: 8,
        }),
      });
    },
  },
    onFileAdded(file) {
      this.file_name = file[0].name
      console.log('File name', file[0].name)
    },

  function_3()
  {
    const cookies=document.cookie.split(";")
    const cookieObj={}
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      const [key, value] = cookie.split('=');
      cookieObj[key] = value;
    }
    this.img_src="/front_end/cache/"+cookieObj['uuid']+"/"+this.file_name+".pre.png"
    console.log(this.img_src)
    console.log(cookieObj['uuid'])
  },

  function_1() {
    const url = "/upload"
    const fileInput = document.getElementById('fileInput')
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);
    fetch(url, {method: 'POST', body: formData}).then(response => response.json())
  },
  function_2()
  {
    fetch('/preview_raster', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({r: 3, g: 2, b: 1}),
      credentials: 'include',
    })
  }
}

</script>

<style >
#uploader{
  left:311px;
  width: 500px;
  border: #64b5f6;

}
.map {
  height: 550px;
  width: 550px;
  margin-left: 400px;
  border: 1px solid #000;
}
</style>
