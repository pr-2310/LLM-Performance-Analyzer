<template>
    <div class="config-container">
        <section class="inference-section">
            <h2>Inference Configuration</h2>
            <div class="config_div">
                <label>Stage:</label>
                <input type="radio" v-model="inference_stage" id="decode" value="decode" checked>
                <label for="decode">Decode</label>
                <input type="radio" v-model="inference_stage" id="prefill" value="prefill">
                <label for="prefill">Prefill</label>
                <input type="radio" v-model="inference_stage" id="chat" value="chat">
                <label for="chat">Chat</label>
            </div>
            <div class="config_div">
                <label>Batchsize:</label>
                <input type="range" min="1" max="256" v-model.lazy="batch_size">
                <input type="number" v-model.lazy="batch_size" min="1" max="256">
            </div>
            <div class="config_div" v-if="inference_stage!='chat'">
                <label>SeqLength:</label>
                <input type="range" min="1" max="4096" v-model.lazy="seq_length">
                <input type="number" v-model.lazy="seq_length" min="1" max="4096">
            </div>
            <div class="config_div" v-else>
                <label>PromptLength:</label>
                <input type="range" min="1" max="4096" v-model.lazy="seq_length">
                <input type="number" v-model.lazy="seq_length" min="1" max="4096">
                <label>GenerateLength:</label>
                <input type="range" min="1" max="4096" v-model.lazy="gen_length">
                <input type="number" v-model.lazy="gen_length" min="1" max="4096">
            </div>
        </section>
        <section class="optimization-section">
            <h2>Optimization Configuration</h2>
            <div class="config_div">
                <label>Weight Quantization:</label>
                <select v-model="w_quant">
                    <option value="FP16">FP16</option>
                    <option value="8-bit">8-bit</option>
                    <option value="4-bit">4-bit</option>
                    <option value="2-bit">2-bit</option>
                    <option value="1-bit">1-bit</option>
                </select>
            </div>
            <div class="config_div">
                <label>Activation Quantization:</label>
                <select v-model="a_quant">
                    <option value="FP16">FP16</option>
                    <option value="8-bit">8-bit</option>
                    <option value="4-bit">4-bit</option>
                    <option value="2-bit">2-bit</option>
                    <option value="1-bit">1-bit</option>
                </select>
            </div>
            <div class="config_div">
                <label>KV Cache Quantization:</label>
                <select v-model="kv_quant">
                    <option value="FP16">FP16</option>
                    <option value="8-bit">8-bit</option>
                    <option value="4-bit">4-bit</option>
                    <option value="2-bit">2-bit</option>
                    <option value="1-bit">1-bit</option>
                </select>
            </div>
            <div class="config_div">
                <label>Use FlashAttention:</label>
                <input type="checkbox" v-model="use_flashattention">
            </div>
        </section>
        <section class="analysis-section">
            <h2>Network-wise Analysis</h2>
            <div>
                <h3>{{ inference_stage }}</h3>
                <div v-for="(value, key) in total_results[inference_stage]" :key="key" class="network-wise-info-item">
                    <span v-if="['bound'].includes(key)">{{ key }}: {{ value }}</span>
                    <span v-else-if="['inference_time'].includes(key)">{{ key }}: {{ strNumberTime(value) }}</span>
                    <span v-else>{{ key }}: {{ strNumber(value) }}</span>
                </div>
                <p>NOTE: The time estimated by the roofline model represents the theoretical performance that the hardware can achieve. 
                The purpose of creating this tool is to help readers gain a clearer understanding of the key factors that influence LLM inference. 
                Only the relative relationships can be referenced. </p>
            </div>
        </section>
    </div>
</template>

<script setup>
import { inject, ref, watch, computed } from 'vue';
import { strNumber,strNumberTime } from '@/utils.js';

const global_update_trigger = inject('global_update_trigger');
const global_inference_config = inject('global_inference_config');
const total_results = inject('total_results');

const inference_stage = ref('decode');
const batch_size = ref(1);
const seq_length = ref(1024);
const gen_length = ref(1);
const w_quant = ref('FP16');
const a_quant = ref('FP16');
const kv_quant = ref('FP16');
const use_flashattention = ref(false);

watch(inference_stage, (new_stage) => {
    console.log("inference_stage", new_stage)
    global_inference_config.value.stage = new_stage
    global_update_trigger.value += 1
})

watch(batch_size, (n) => {
    console.log("inference_stage", n)
    global_inference_config.value.batch_size = n
    global_update_trigger.value += 1
})

watch(seq_length, (n) => {
    console.log("seq_length", n)
    global_inference_config.value.seq_length = n
    global_update_trigger.value += 1
})

watch(w_quant, (n) => {
    console.log("w_quant", n)
    global_inference_config.value.w_quant = n
    global_update_trigger.value += 1
})

watch(a_quant, (n) => {
    console.log("a_quant", n)
    global_inference_config.value.a_quant = n
    global_update_trigger.value += 1
})

watch(kv_quant, (n) => {
    console.log("kv_quant", n)
    global_inference_config.value.kv_quant = n
    global_update_trigger.value += 1
})

watch(use_flashattention, (n) => {
    console.log("use_flashattention", n)
    global_inference_config.value.use_flashattention = n
    global_update_trigger.value += 1
})

watch(gen_length, (n) => {
    console.log("gen_length", n)
    global_inference_config.value.gen_length = n
    global_update_trigger.value += 1
})

</script>

<style>

.config-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    background-color: #fffdfd; /* Neutral background for a professional look */
}

.config_div {
    border-top: 1px solid #d3d3d3; /* Light gray for a subtle separation */
    padding: 10px;
    background-color: #ffffff; /* White background for sections for a clean look */
}

.hover_color {
    color: #007bff; /* Blue for a professional hover effect */
    cursor: pointer;
}
.network-wise-info-item {
    padding: 3px;
    border-top: 1px solid #d3d3d3; /* Consistent with other dividers */
    color: #212529; /* Standard dark text for professional readability */
}

</style>