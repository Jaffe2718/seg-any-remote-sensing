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
      <img src="public/logo.png" alt="" id="logo-img">
    </q-btn>
  </q-btn-group>
</div>
</template>

<script>
export default {
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
    }
  }
}

</script>

<style >
#bt-dr{
  width: 240px;
  height: 65px;
}
#menu-function-btn{
  width: 300px;
  height: 100px;
}
#btn-group{
  height: 65px;
}
#logo {
  width: 223px;
  height: 65px;
}
#logo-img{
  width: 235px;
  height: 66px;
  margin-left: -1.5px;
  margin-top: -5px;
}

</style>
