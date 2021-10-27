<template>
  <div class="home">
    <h2>力向导图示例</h2>
    <ForceDirected id="mytest"  :nodes="nodes" :edges="edges"></ForceDirected>
  </div>
</template>

<script>
// @ is an alias to /src
import ForceDirected from "@/components/ForceDirected.vue";

export default {
  name: "Home",
  components: {
    ForceDirected,
  },
  data() {
    return {
      // 节点集
      nodes : [
        { name: "天津大学" },
        { name: "智能与计算学部" },       
        { name: "小超" },
        { name: "小丽" },
        { name: "小华" },
        { name: "组长" },
        { name: "计算机学" },
        { name: "老王" },
        { name: "图形学" },
        { name: "SIGGRAPH" },
      ],
      // 边集
      edges : [
        { source: 0, target: 4, relation: "学生", value: 1 },
        { source: 0, target: 2, relation: "学生", value: 2 },
        { source: 0, target: 3, relation: "学生", value: 1 },
        { source: 0, target: 1, relation: "分院", value: 2 },
        { source: 4, target: 5, relation: "职务", value: 1.5 },
        { source: 2, target: 3, relation: "校友", value: 2.5 },
        { source: 3, target: 4,  relation: "校友", value: 1.7 },
        { source: 2, target: 7,  relation: "导师", value: 2 },
        { source: 8, target: 7,  relation: "研究", value: 1.5 },
        { source: 8, target: 6,  relation: "子学科", value: 2 },
        { source: 8, target: 9,  relation: "期刊", value: 1.7 },
        
      ],
      
    };
  },
};
</script>
