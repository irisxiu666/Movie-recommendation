<template>
  <div
    class="chart-container"
    style="margin-bottom: 50px; width: 100%; height: 500px"
    ref="el"
  ></div>
</template>

<script lang="ts" setup>
import { onMounted, ref, watch } from "vue";
import request from "/@/utils/request";
const props = defineProps(["api"]);
const el = ref(null);
let chart: any = null;
const load = () => {
  request.get(props.api).then((res) => {
    if (typeof res.data === "string") {
      let no = eval("(" + res.data + ")");
      chart.setOption(no);
    } else {
      chart.setOption(res.data);
    }
  });
};
watch(
  () => props.api,
  () => {
    load();
  }
);
onMounted(() => {
  chart = echarts.init(el.value as unknown as HTMLElement, "white", {
    renderer: "canvas",
  });
  window.addEventListener("resize", () => {
    chart.resize();
  });
  load();
});
</script>