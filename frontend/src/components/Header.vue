<template>
    <div class="title">
        <a class="hover-bold">Comparitive Analysis of LLMs</a>
        v{{ version }}
    </div>
    <div class="header_button">
        |
        <span>LLM Model: </span>
        <select v-model="select_model_id" class="dropdown-style">
            <option v-for="model_id in avaliable_model_ids" :value="model_id">{{ model_id }}</option>
        </select>
        <span> | </span>
        <span>Hardware: </span>
        <select v-model="select_hardware" class="dropdown-style">
            <option v-for="hardware in avaliable_hardwares" :value="hardware">{{ hardware }}</option>
        </select>
    </div>
    <div>
        <span> | </span>
        <span>Server: </span>
        <select v-model="ip_port" class="dropdown-style">
            <option value="">gcp_endpoint</option>
            <!-- <option value="https://us-central1-aiplatform.googleapis.com/v1/projects/604007508233/locations/us-central1/endpoints/58166364132605952:predict">https://us-central1-aiplatform.googleapis.com/v1/projects/604007508233/locations/us-central1/endpoints/58166364132605952</option> -->
            <option value="127.0.0.1:5000">127.0.0.1</option>
        </select>
    </div>
</template>

<script setup>
import { inject, ref, watch, onMounted } from 'vue';
import axios from 'axios'
const model_id = inject('model_id');
const hardware = inject('hardware');
const global_update_trigger = inject('global_update_trigger');
const ip_port = inject('ip_port');

const avaliable_hardwares = ref([]);
const avaliable_model_ids = ref([]);

const version = ref(llm_viewer_frontend_version)


function update_avaliable() {
    const url = 'http://' + ip_port.value + '/get_avaliable'
    axios.get(url).then(function (response) {
        console.log(response);
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
    console.log("select_model_id", n)
    model_id.value = n
    global_update_trigger.value += 1
})

var select_hardware = ref('nvidia_V100');
watch(select_hardware, (n) => {
    console.log("select_hardware", n)
    hardware.value = n
    global_update_trigger.value += 1
})

watch(ip_port, (n) => {
    console.log("ip_port", n)
    update_avaliable()
})


</script>

<style scoped>
.header_button button {
    font-size: 1.0rem;
    margin: 5px;
    padding: 5px;
    border-radius: 5px;
    border: 1px solid #000000;
    cursor: pointer;
}

.header_button button:hover {
    color: #fff;
    background-color: #000;
}

.header_button button:active {
    color: #fff;
    background-color: #000;
}

.active {
    color: #fff;
    background-color: #5b5b5b;
}

.title {
    font-size: 18px;
    text-align: left;
}

.hover-bold{
    color: inherit;
}

.hover-bold:hover {
    font-weight: bold;
}

.float-info-window {
    position: absolute;
    top: 80px;
    left: 40%;
    height: auto;
    width: 30%;
    background-color: #f1f1f1ed;
    z-index: 999;
}

.dropdown-style {
    padding: 5px;
    border-radius: 5px;
    background-color: #e8e8f0;
    color: #333;
}

.dropdown-style:hover {
    background-color: #d0d0f0;
    color: #000;
}

</style>