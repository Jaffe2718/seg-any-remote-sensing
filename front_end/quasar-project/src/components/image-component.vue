<template>
  <div><button-component ref="sonRef"></button-component></div>
  <div id="image_all">
    <div id="image_all2">
      <div class="JZ">
        <q-uploader
          ref="uploader"
          id="uploader"
          url="/upload"
          no-thumbnails
          square
          name="file"
          @added="onFileAdded"
        />
        <div><q-btn @click="function_3" :ripple="false" color="secondary"  no-caps size="20px" style="width: 310px">点击此处加载图片</q-btn></div>
      </div>
      <div id="switch_map">
        <q-btn @click="changeMap(1)">原图</q-btn>
        <q-btn @click="changeMap(2)">分割过后的图</q-btn>
      </div>
      <div id="map" class="map"></div>
    </div>
  </div>

    <!--    <div><q-btn @click="function_2">加载png</q-btn></div>-->
    <SPS @fatherMethod="add_preview" :use_map="map"></SPS>

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
import ButtonComponent from "components/button-component.vue";
import SPS from "components/seg-param-steps.vue"
export default {
  components:{
    ButtonComponent,SPS
  },
  name: "image-component",
  setup() {
    return {
      model: ref(null),
    }
  },
  data(){
    return{
      file_name:"logo.png",
      image_src:"https://imgs.xkcd.com/comics/online_communities.png",
      map:null,
      test_child:"Hello World!"
    }
  },
  computed: {
    buffer() {
      return buffer
    }
  },
  mounted() {
    this.initMap();
  },
  methods: {
    changeMap(data){
      if(data==1){
        this.map.getLayers().item(0).setVisible(true);
        this.map.getLayers().item(1).setVisible(false);
      }else {
        this.map.getLayers().item(1).setVisible(true);
        this.map.getLayers().item(0).setVisible(false);
      }
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
    },
    onFileAdded(file) {
      this.file_name = file[0].name
    },
    function_3()
    {
      fetch('/preview_raster', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({r: 3, g: 2, b: 1}),
        credentials: 'include',
      }).then(status=>{
        const cookies=document.cookie.split(";")
        const cookieObj={}
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          const [key, value] = cookie.split('=');
          cookieObj[key] = value;
        }
        this.img_src="/front_end/cache/"+cookieObj['uuid']+"/"+this.file_name+".pre.png"
        this.image_src="/front_end/cache/"+cookieObj['uuid']+"/"+this.file_name+".pre.png"
        const extent = [100, 100, 500, 480];
        const projection = new Projection({
          code: 'xkcd-image',
          units: 'pixels',
          extent: extent,
        });
        const layer=new ImageLayer({
          source:new Static({
            url: this.image_src,//到时候替换成image_src
            projection: projection,
            imageExtent: extent,
          })
        })
        this.map.addLayer(layer)
      })
        .catch(error=>{
          console.log(error)
        })

    },
    add_preview(file_name)
    {

    },
    initMap: function ()
    {
      const extent = [100, 100, 500, 480];
      const projection = new Projection({
        code: 'xkcd-image',
        units: 'pixels',
        extent: extent,
      });
      this.map = new Map({
        layers: [
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
}
</script>
<style >
.map {
  height: 620px;
  width: 850px;
  //border: 1px solid #000;
  box-shadow: 0 0 3px ;
  position: relative;
  left: 400px;
  top:30px;
}
#content_data{
  width: 400px;
  height: 680px;
  border: 1px solid #000;
  margin-top: -680px;
}
.JZ{
  position: absolute;
  top: 30px;
  left: 50px;
}
#switch_map{
  position: absolute;
  top:30px;
  left:1074px;
  z-index: 9;
}
#image_all{
  height: 680px;
  margin: 10px 15px 0 15px;
  box-shadow: 0 0 5px rgb(200,200,200);
  position: relative;
}
#image_all2{
  position: relative;
  left:50px
}
</style>
