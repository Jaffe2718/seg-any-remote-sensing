<template>
<!--  <button-component></button-component>-->
  <image-component></image-component>

</template>

<script>
import { defineComponent, ref } from 'vue'
// import ButtonComponent from "components/button-component.vue";
import ImageComponent from "components/image-component.vue";

export default defineComponent({
  name: 'MainLayout',
  components: {ImageComponent},
})
</script>
