<template>
    <div class="left_control">
        <Config></Config>
    </div>
</template>

<script setup>
import Config from "./left_controls/Config.vue"
import { inject, onMounted } from 'vue';

const model_id = inject('model_id');

onMounted(() => {
    console.log("LeftControl onMounted", model_id.value)
})

</script>

<style>
.input_config {
    border: 1px solid #ccc;
    margin: 3px;
}

.left_control {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    width: 25%;
    height: 100%;
    background-color: #e8e8f0;
    border-left: 5px solid #a2a2d0;
    overflow-y: auto;
    padding: 10px;
}
</style>