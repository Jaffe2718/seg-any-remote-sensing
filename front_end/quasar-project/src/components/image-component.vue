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
<!--  <div id="img_display" >-->
<!--    hello-->
<!--    <q-img src="logo.png"></q-img>-->
<!--  </div>-->
<!--  <q-btn id="test_fetch" @click="function_2"> 测试png转换</q-btn>-->
<!--  <q-btn @click="function_3">测试cookie</q-btn>-->
<!--&lt;!&ndash; <div><q-img v-bind:src="img_src" alt="图片"></q-img></div>&ndash;&gt;-->
<!--&lt;!&ndash;  <div id="img_load"><q-img src="logo.png"></q-img></div>&ndash;&gt;-->
<!--  <v-viewer id="img_load"><q-img src="logo.png"></q-img></v-viewer>-->
</template>
<script>
import {ref} from "vue";
import * as buffer from "buffer";
import 'viewerjs/dist/viewer.css'
import {BingMaps, ImageStatic} from 'ol/source';
import { Tile as TileLayer } from 'ol/layer';
import Map from 'ol/Map';
import View from 'ol/View';
import {ZoomToExtent} from "ol/control";
import {transform} from "ol/proj";
import * as source from "ol/source";
import ImageLayer from "ol/layer/Image";
export default {
  name: "image-component",
  data(){
    return{
      img_src:"",
      file_name:"",
      map:null,
      imgX: 0, // 当前地图宽
      imgY: 0, // 当前地图高
      viewer:null
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
    // this.initMap();
  },
  methods: {
    // InitMap()
    // {
    //   let extent = [0, 0, this.imgX, this.imgY];  // 获取图片的宽高
    //   this.map = new Map({
    //     target: 'map', // 地图容器的ID
    //     layers: [
    //       new ImageLayer({
    //         source:new ImageStatic({
    //           url:"https://imgs.xkcd.com/comics/online_communities.png",
    //           imageExtent:extent
    //         })
    //       })
    //     ], // 初始时没有图层
    //     view: new View({
    //       center: [0, 0], // 地图中心点坐标
    //       zoom: 2 // 初始缩放级别
    //     })
    //   });
    // },
    // initMap: function () {
    //   this.map = new Map({
    //     target: 'map',
    //     layers: [
    //       new TileLayer({
    //         source: new BingMaps({
    //           key: 'AhHD9H_H9z-Oikv-CJcNCmuXoh-Q1U6NZj0rO63sRtWscwX-5FmhAsss7-GJv1lW',
    //           imagerySet: 'Aerial',
    //         }),
    //       }),
    //     ],
    //     view: new View({
    //       center: [112.98,28.19],
    //       zoom: 6,
    //
    //     }),
    //     //controls
    //   });
    //   this.viewer=this.map.getView();
    //   this.viewer.setCenter(transform([112.945,28.190],'EPSG:4326', 'EPSG:3857'))
    //   this.viewer.setZoom(17.2)
    //
    // },
    show(){
      const ViewerDom = document.getElementById('img_load')
      const viewer = new Viewer(ViewerDom, {
        container:ViewerDom,
        magnifierSize: '200px', // 放大镜大小
        transitionDuration: '0.5s', // 过渡效果持续时间
        inline:true,
        zoomable:true
      })
      console.log(viewer)
    },
    onFileAdded(file){
      this.file_name=file[0].name
      console.log('File name',file[0].name)
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
    },


}

</script>

<style >
#uploader{
  left:311px;
  width: 500px;
  border: #64b5f6;

}
.map {
  height: 750px;
  width: 1200px;
}
#img_display{
  background-color: red;
  position: absolute;
  left:310px;
  width: 800px;
  height: 500px;
  font-size: 18px;
  line-height: 30px;
  font-weight: bold;
  color: white;
  padding: 40px;
  border: 10px;
  box-shadow:
    inset #64b5f6 0 0 0 5px
}
</style>
