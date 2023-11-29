<template>
  <div class="menu-drop">
    <q-btn-group id="btn-group">
      <q-btn-dropdown id="bt-dr" color="light-blue-7" label="菜单栏">
        <q-list>
          <q-item id="menu-function-btn" clickable v-close-popup @click="menu_function_1">
            <q-item-section>
              <q-item-label>功能一</q-item-label>
            </q-item-section>
          </q-item>
          <q-item id="menu-function-btn" clickable v-close-popup @click="menu_function_2">
            <q-item-section>
              <q-item-label>功能二</q-item-label>
            </q-item-section>
          </q-item>
          <q-item id="menu-function-btn" clickable v-close-popup @click="menu_function_3">
            <q-item-section>
              <q-item-label>功能三</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>
      <q-btn id="logo" @click="logo_function">
        <img src="logo.png" alt="" id="logo-img">
      </q-btn>
      <q-btn id="btn_exp" label="使用说明" color="light-blue-7" @click="explain = true" />
      <q-dialog v-model="explain" transition-show="rotate" transition-hide="rotate">
        <q-card>
          <q-card-section>
            <div class="text-h6">地信王的自我介绍</div>
          </q-card-section>
          <q-card-section class="q-pt-none">
            <p>大家好，我是王旭升，一个普通的小学生。我的名字寓意着旭日东升，每天都有新的希望和开始。 虽然我有些胆小和懦弱，但我总是努力去尝试新事物，去挑战自己的极限。我喜欢装逼，喜欢摆出各种造型，但我更喜欢帮助他人，为同学们排忧解难，尤其是快乐婆。 我非常喜欢奥特曼，他是我心目中的英雄。他不仅有强大的力量，还有坚定的信念和高尚的品质。我希望自己也能像他一样勇敢、正义、无私。 我认为我是全世界最帅的人，这不是自恋，而是自信。我有一双明亮的眼睛，一个挺拔的鼻子，和一张能说会道的嘴巴。我会时常照镜子，欣赏自己的帅气，也会学习各种表情和造型，为自己的形象加分。 总之，我是一个喜欢挑战自己、追求快乐、充满自信的小学生。希望大家能够喜欢我，和我一起度过愉快的时光。谢谢大家！</p>
          </q-card-section>
          <q-card-actions align="right">
            <q-btn flat label="fuck me" color="primary" v-close-popup />
            <q-btn flat label="i am sb" color="primary" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>
      <q-btn-dropdown id="btn_url" color="light-blue-7" label="常用链接">
        <q-list>
          <q-item id="url-function-btn" clickable v-close-popup href="http://dlkx.hunnu.edu.cn/info/1767/5240.htm" target="_blank">
            <q-item-section>
              <q-item-label>链接一</q-item-label>
            </q-item-section>
          </q-item>
          <q-item id="url-function-btn" clickable v-close-popup href="https://yxysz.sysu.edu.cn/zh-hans/node/242" target="_blank" >
            <q-item-section>
              <q-item-label>链接二</q-item-label>
            </q-item-section>
          </q-item>
          <q-item id="url-function-btn" clickable v-close-popup href="https://www.ais.cn/mentor/mentorDetail/9eb9386d-5e3c-11ec-b045-a85e45a23623" target="_blank" >
            <q-item-section>
              <q-item-label>链接三</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>
      <q-btn id="btn_about" color="light-blue-7" @click="about = true" label="关于我们"/>
      <q-dialog v-model="about" transition-show="rotate" transition-hide="rotate">
        <q-card>
          <q-card-section>
            <div class="text-h6">地信王的自我介绍</div>
          </q-card-section>
          <q-card-section class="q-pt-none">
            <p>大家好，我是王旭升，一个普通的小学生。我的名字寓意着旭日东升，每天都有新的希望和开始。 虽然我有些胆小和懦弱，但我总是努力去尝试新事物，去挑战自己的极限。我喜欢装逼，喜欢摆出各种造型，但我更喜欢帮助他人，为同学们排忧解难，尤其是快乐婆。 我非常喜欢奥特曼，他是我心目中的英雄。他不仅有强大的力量，还有坚定的信念和高尚的品质。我希望自己也能像他一样勇敢、正义、无私。 我认为我是全世界最帅的人，这不是自恋，而是自信。我有一双明亮的眼睛，一个挺拔的鼻子，和一张能说会道的嘴巴。我会时常照镜子，欣赏自己的帅气，也会学习各种表情和造型，为自己的形象加分。 总之，我是一个喜欢挑战自己、追求快乐、充满自信的小学生。希望大家能够喜欢我，和我一起度过愉快的时光。谢谢大家！</p>
          </q-card-section>
          <q-card-actions align="right">
            <q-btn flat label="fuck me" color="primary" v-close-popup />
            <q-btn flat label="i am sb" color="primary" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </q-btn-group>
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
</style>
