<template>
  <div id="img_data">
    <q-uploader
      url="/upload"
    />

  </div>
  <div>
    <q-uploader url="/upload_cfg"/>
  </div>
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
      }
  }
}
</script>

<style scoped>
</style>
