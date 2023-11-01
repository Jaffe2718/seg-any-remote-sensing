<template>
  <button-component></button-component>
</template>

<script>
import { defineComponent, ref } from 'vue'
import ButtonComponent from "components/button-component.vue";
export default defineComponent({
  name: 'MainLayout',
  components: {ButtonComponent},
})
</script>
