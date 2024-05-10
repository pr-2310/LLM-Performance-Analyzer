<template>
    <div class="title">
        <a class="hover-bold">Comparitive Analysis of LLMs</a>
        <!-- v{{ version }} -->
    </div>
    <div class="header_button">
        <span style="color: #333333;"> | </span>
        <span class="bold-and-stylish">Model : </span>
        <select v-model="select_model_id">
            <option v-for="model_id in avaliable_model_ids" :value="model_id">{{ model_id }}</option>
        </select>
        <span style="color: #333333;"> | </span>
        <span class="bold-and-stylish">Hardware: </span>
        <select v-model="select_hardware">
            <option v-for="hardware in avaliable_hardwares" :value="hardware">{{ hardware }}</option>
        </select>
        <span style="color: #333333;"> | </span>
        <span class="bold-and-stylish">Server: </span>
        <select v-model="ip_port">
            <option value="">gcp_endpoint</option>
            <option value="127.0.0.1:5000">127.0.0.1</option>
        </select>
    </div>
</template>

<script setup>
import { inject, ref, watch, onMounted } from 'vue';
import axios from 'axios';

const model_id = inject('model_id');
const hardware = inject('hardware');
const global_update_trigger = inject('global_update_trigger');
const ip_port = inject('ip_port');

const avaliable_hardwares = ref([]);
const avaliable_model_ids = ref([]);

const version = ref(llm_viewer_frontend_version)

const is_show_help = ref(false)

function update_avaliable() {
    const url = 'http://' + ip_port.value + '/get_avaliable'
    axios.get(url).then(function (response) {
        avaliable_hardwares.value = response.data.avaliable_hardwares
        avaliable_model_ids.value = response.data.avaliable_model_ids
    })
        .catch(function (error) {
            console.log("error in get_avaliable");
            console.log(error);
        });
}

onMounted(() => {
    console.log("Header mounted")
    update_avaliable()
})

var select_model_id = ref('meta-llama/Llama-2-7b-hf');
watch(select_model_id, (n) => {
    model_id.value = n
    global_update_trigger.value += 1
})

var select_hardware = ref('nvidia_V100');
watch(select_hardware, (n) => {
    hardware.value = n
    global_update_trigger.value += 1
})

watch(ip_port, (n) => {
    update_avaliable()
})
</script>

<style scoped>
.header_button button {
    font-size: 1.0rem;
    margin: 5px;
    padding: 5px;
    border-radius: 5px;
    border: none;
    background-color: #4a90e2;
    color: #ffffff;
    cursor: pointer;
    transition: background-color 0.3s;
}

.header_button button:hover {
    background-color: #357abd;
}

.header_button button:active {
    background-color: #2a5c9a;
}

.active {
    background-color: #2a5c9a;
}

.title {
    font-size: 20px;
    color: #333333;
    text-align: left;
    font-weight: bold;
    padding-right: 10px;
}

.bold-and-stylish {
    font-weight: bold;
    color: #333333;
    font-size: 16px;
    margin-right: 5px;
}

.hover-bold {
    color: #333333;
    transition: font-weight 0.3s;
}

.hover-bold:hover {
    font-weight: bold;
}

select {
    margin-bottom: 10px;
    margin-top: 10px;
    outline: 1;
    background: #fff;
    border: #000;
    color: #000;
    border: 1px solid crimson;
    padding: 8px;
    border-radius: 10px;
}

.float-info-window {
    color: #333333;
    position: absolute;
    top: 60px;
    left: 75%;
    transform: translateX(-50%);
    width: 40%;
    background-color: #f8f8f8;
    border: 1px solid #ddd;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 20px;
    z-index: 999;
}

.header_button {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 14px;
}

div {
    margin: 5px 0;
    color: #D6DBDF;
}

a {
    color: #357abd;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}
</style>