<template>
  <div id="img_data">
    <q-uploader
      url="/upload"
    />

  </div>
  <div>
    <q-uploader url="/upload_cfg"/>
  </div>
  <q-btn id="test_fetch" @click="function_2"> 测试png转换</q-btn>
</template>

<script>
import {ref} from "vue";

export default {
    name: "image-component",
  setup () {
    return {
      model: ref(null)
    }
  },
  methods:{
      function_1(){
        const url="/upload"
        const fileInput =document.getElementById('fileInput')
        const file=fileInput.files[0];
        const formData = new FormData();
        formData.append('file',file);
        fetch(url,{method:'POST',body:formData}).then(response =>response.json())
      },
      function_2(){
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
}
</script>

<style scoped>
</style>
