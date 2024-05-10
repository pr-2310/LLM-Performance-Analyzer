<template>
    <h3>Inference Configuration</h3>
    <div class="config_div">
      <span>Stage:</span>
      <input
        type="radio"
        v-model="inference_stage"
        id="decode"
        value="decode"
        checked
      />
      <label for="decode">Decode</label>
      <input
        type="radio"
        v-model="inference_stage"
        id="prefill"
        value="prefill"
      />
      <label for="prefill">Prefill</label>
      <input type="radio" v-model="inference_stage" id="chat" value="chat" />
      <label for="prefill">Chat</label>
    </div>
    <div class="config_div">
      <span>Batchsize:</span>
      <input
        type="range"
        min="1"
        max="256"
        value="1"
        v-model.lazy="batch_size"
        style="width: 80px"
      />
      <input
        type="number"
        v-model.lazy="batch_size"
        min="1"
        max="256"
        style="
          width: 40px;
          background: #fff;
          color: #000;
          padding: 5px;
          border-radius: 10px;
        "
      />
    </div>
    <!-- <div class="config_div" v-if="inference_stage!=chat"> -->
    <div class="config_div" v-if="inference_stage != 'chat'">
      <span>Seq-Length:</span>
      <input
        type="range"
        v-model.lazy="seq_length"
        min="1"
        max="4096"
        value="1024"
        style="width: 80px"
      />
      <!-- <span id="seq_length">1024</span> -->
      <input
        type="number"
        v-model.lazy="seq_length"
        min="1"
        max="4096"
        style="
          width: 45px;
          outline: 1;
          background: #fff;
          color: #000;
          padding: 5px;
          border-radius: 10px;
        "
      />
    </div>
    <div class="config_div" v-else>
      <span>PromptLength:</span>
      <input
        type="range"
        min="1"
        max="4096"
        value="1024"
        v-model.lazy="seq_length"
        style="width: 80px"
      />
      <!-- <span id="seq_length">1024</span> -->
      <input
        type="number"
        v-model.lazy="seq_length"
        min="1"
        max="4096"
        style="
          width: 45px;
          outline: 1;
          background: #fff;
          color: #000;
          padding: 5px;
          border-radius: 10px;
        "
      />
      <br />
      <br />
      <span>GenerateLength:</span>
      <input
        type="range"
        min="1"
        max="4096"
        value="1024"
        v-model.lazy="gen_length"
        style="width: 80px"
      />
      <!-- <span id="seq_length">1024</span> -->
      <input
        type="number"
        v-model.lazy="gen_length"
        min="1"
        max="4096"
        style="
          width: 45px;
          outline: 1;
          background: #fff;
          color: #000;
          padding: 5px;
          border-radius: 10px;
        "
      />
    </div>
    <!-- <div class="config_div">
          Generation Length:
          <input type="range" min="1" max="4096" value="1024" oninput="gen_length.innerText = this.value">
          <p id="gen_length">1</p>
      </div> -->
    <h3>Optimization Configuration</h3>
    <div class="config_div">
      <span style="padding-right: 10px">Weight Quantization : </span>
      <select v-model="w_quant">
        <option value="FP16">FP16</option>
        <option value="8-bit">8-bit</option>
        <option value="4-bit">4-bit</option>
        <option value="2-bit">2-bit</option>
        <option value="1-bit">1-bit</option>
      </select>
    </div>
    <div class="config_div">
      <span style="padding-right: 10px">Activation Quantization : </span>
      <select v-model="a_quant">
        <option value="FP16">FP16</option>
        <option value="8-bit">8-bit</option>
        <option value="4-bit">4-bit</option>
        <option value="2-bit">2-bit</option>
        <option value="1-bit">1-bit</option>
      </select>
    </div>
    <div class="config_div">
      <span style="padding-right: 10px">KV Cache Quantization : </span>
      <select v-model="kv_quant">
        <option value="FP16">FP16</option>
        <option value="8-bit">8-bit</option>
        <option value="4-bit">4-bit</option>
        <option value="2-bit">2-bit</option>
        <option value="1-bit">1-bit</option>
      </select>
    </div>
    <div class="config_div">
      <span style="padding-right: 10px">Use FlashAttention : </span>
      <input type="checkbox" v-model="use_flashattention" />
    </div>
  
    <!-- <div class="config_div">
          Use Flash Attention
          <input type="checkbox">
      </div>
      <div class="config_div">
          Decoding Method
          <select>
              <option value="Greedy">Greedy</option>
          </select>
      </div> -->
    
    <div>
      <h3>Network-Wise Analysis</h3>
      <h3>{{ inference_stage }}</h3>
      <div
        style="padding-left: 10px;font-size: 15px;"
        v-for="(value, key) in total_results[inference_stage]"
        :key="key"
        class="network-wise-info-item"
      >
        <span v-if="['bound'].includes(key)"
          ><strong>{{ key }} : </strong> {{ value }}</span
        >
        <span v-else-if="['inference_time'].includes(key)"
          ><strong>{{ key }} : </strong> {{ strNumberTime(value) }}</span
        >
        <span v-else
          ><strong>{{ key }} : </strong> {{ strNumber(value) }}</span
        >
      </div>
  
      
    </div>
    
  </template>
  
  <script setup>
  import { inject, ref, watch, computed } from "vue";
  import { strNumber, strNumberTime } from "@/utils.js";
  
  const global_update_trigger = inject("global_update_trigger");
  
  const global_inference_config = inject("global_inference_config");
  const total_results = inject("total_results");
  
  const inference_stage = ref("decode");
  const batch_size = ref(1);
  const seq_length = ref(1024);
  const gen_length = ref(1);
  const w_quant = ref("FP16");
  const a_quant = ref("FP16");
  const kv_quant = ref("FP16");
  const use_flashattention = ref(false);
  
  watch(inference_stage, (new_stage) => {
    console.log("inference_stage", new_stage);
    global_inference_config.value.stage = new_stage;
    global_update_trigger.value += 1;
  });
  
  watch(batch_size, (n) => {
    console.log("inference_stage", n);
    global_inference_config.value.batch_size = n;
    global_update_trigger.value += 1;
  });
  
  watch(seq_length, (n) => {
    console.log("seq_length", n);
    global_inference_config.value.seq_length = n;
    global_update_trigger.value += 1;
  });
  
  watch(w_quant, (n) => {
    console.log("w_quant", n);
    global_inference_config.value.w_quant = n;
    global_update_trigger.value += 1;
  });
  
  watch(a_quant, (n) => {
    console.log("a_quant", n);
    global_inference_config.value.a_quant = n;
    global_update_trigger.value += 1;
  });
  
  watch(kv_quant, (n) => {
    console.log("kv_quant", n);
    global_inference_config.value.kv_quant = n;
    global_update_trigger.value += 1;
  });
  
  watch(use_flashattention, (n) => {
    console.log("use_flashattention", n);
    global_inference_config.value.use_flashattention = n;
    global_update_trigger.value += 1;
  });
  
  watch(gen_length, (n) => {
    console.log("gen_length", n);
    global_inference_config.value.gen_length = n;
    global_update_trigger.value += 1;
  });
  </script>
  
  <style>
  .config_div {
    border-bottom: 1px solid #e2e2e2;
    padding: 10px;
  }
  
  h3 {
    color: #333333;
    padding-left: 10px;
  }
  
  label {
    color: #333333;
  }
  
  span {
    color: #333333;
    font-weight: bold;
  }
  
  select {
    outline: 1;
    background: #fff;
    color: #000;
    padding: 5px;
    border-radius: 10px;
  }
  
  .hover_color {
    color: #0000ff;
    cursor: pointer;
  }
  
  .network-wise-info-item {
    padding: 3px;
    border-top: 1px solid #e2e2e2;
  }
  </style>
  