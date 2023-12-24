<template>
  <div class="menu-drop">
    <div id="logo" @click="logo_function">
      <img src="logo2.png" alt="" id="logo-img">
    </div>

      <q-btn id="btn_exp" label="使用说明" color="light-blue-7" @click="explain = true" />
      <q-dialog v-model="explain" transition-show="rotate" transition-hide="rotate">
        <q-card>
          <q-card-section>
            <div class="text-h6">怎么用？</div>
          </q-card-section>
          <q-card-section class="q-pt-none">
            <p>请询问专业人员！</p>
          </q-card-section>
          <q-card-actions align="right">
            <q-btn flat label="OK" color="primary" v-close-popup />
            <q-btn flat label="CLOSE" color="primary" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>
      <q-btn id="btn_about" color="light-blue-7" @click="about = true" label="关于我们"/>
      <q-dialog v-model="about" transition-show="rotate" transition-hide="rotate">
        <q-card>
          <q-card-section>
            <div class="text-h6">我们组</div>
          </q-card-section>
          <q-card-section class="q-pt-none">
            <p>我们组是这样的</p>
          </q-card-section>
          <q-card-actions align="right">
            <q-btn flat label="OK" color="primary" v-close-popup />
            <q-btn flat label="CLOSE" color="primary" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>

  </div>

</template>

<script>
import {ref} from 'vue'
export default {
  data()
  {
    return{

    }
  },
  setup(){
    //const image_src=ref("Hello World!")
    return{
      explain: ref(false),
      about:ref(false)
    }
  },
  name: "button-component",
  methods:{

    menu_function_1(){
      alert("该功能开发中！")
    },
    menu_function_2(){
      alert("该功能开发中！")
    },
    menu_function_3(){
      alert("该功能开发中！")
    },
    logo_function(){
      window.open("https://www.hunnu.edu.cn/")
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
}
</script>
<style >
#uploader{
  width: 310px;
  border: #64b5f6;
}
#bt-dr{
  width: 310px;
  height: 65px;
}
#menu-function-btn{
  width: 310px;
  height: 100px;
}
#btn-group{
  height: 65px;
}
#logo {
  width: 310px;
  height: 65px;
  float: right;
}
#logo-img{
  width: 280px;
  height: 66px;
  margin-left: -1.5px;
  margin-top: -5px;
}
#btn_exp{
  width: 310px;
  height: 65px;
}
#btn_url{
  width: 310px;
  height: 65px;
}
#btn_about{
  width: 310px;
  height: 65px;
}
#url-function-btn{
  width: 300px;
  height: 100px;
}
.menu-drop{
  background: dodgerblue;
  box-shadow: 0 0 5px 2px rgb(100,100,100);
}
</style>
