<template>
  <button-component></button-component>
  <image-component></image-component>
  <MapPng></MapPng>
</template>

<script>
import { defineComponent, ref } from 'vue'
import ButtonComponent from "components/button-component.vue";
import ImageComponent from "components/image-component.vue";
import MapPng from "components/MapPng.vue";
export default defineComponent({
  name: 'MainLayout',
  components: {ImageComponent, ButtonComponent,MapPng},
})
</script>
