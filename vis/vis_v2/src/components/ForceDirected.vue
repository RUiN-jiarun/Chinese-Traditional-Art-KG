<template> 
  <svg 
    :id="id" 
    :width="width" 
    :height="height" 
    @mouseover.prevent="svgMouseover"
    @mouseout="svgMouseout"
  />  
</template>

<script>
import * as d3 from "d3";

export default {
  name: "ForceDirected",
  props: {
    id: String,
    width: {
      type: String,
      default: String(window.innerWidth),
    },
    height: {
      type: String,
      default: String(window.innerHeight),
    },
    nodes: Array,
    links: Array,
    strength: {
      type: Number,
      default: -200,
    },
    fontSize: {
      type: String,
      default: "12px",
    },
  },

  data() {
    return {
      selection: {
        links: [],
        nodes: [],
      },
      pinned: [],     
    };
  },

  mounted() {
    this.init();
  },

  watch: {
    load() {
      this.init();
    },
  },

  methods: {
    init() {
      // let marge = { top: 30, bottom: 30, left: 30, right: 30 };
      let svg = d3.select("svg");
      let width = this.width;
      let height = this.height;
      let g = svg
        .append("g");
      // 准备数据
      // 节点集
      let nodes = this.nodes;
      // 边集
      let links = this.links;
      // 设置一个颜色比例尺
      let colorScale = d3
        .scaleOrdinal()
        .domain(d3.range(nodes.length))
        .range(d3.schemeCategory10);
      // 新建一个力导向图
      let forceSimulation = d3
        .forceSimulation()
        .force("link", d3.forceLink())
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter());
      // 生成节点数据
      forceSimulation.nodes(nodes).on("tick", ticked);
      // 生成边数据
      forceSimulation
        .force("link")
        .links(links)
        .distance(function (d) {
          // 每一边的长度
          return 150 / d.value ;
        });
      // 设置图形中心位置
      forceSimulation
        .force("center")
        .x(width / 2)
        .y(height / 2);
      // 设置作用力
      forceSimulation
        .force("charge", d3.forceManyBody().strength(this.strength));
        
      // 绘制边
      let glinks = g
        .append("g")
        .selectAll("line")
        .data(links)
        .enter()
        .append("line")
        .attr("stroke", "lightgray")
        .attr("stroke-width", 2);
      // 边上的文字
      let linksText = g
        .append("g")
        .selectAll("text")
        .data(links)
        .enter()
        .append("text")
        .text(function (d) {
          return d.relation;
        })
        .style("font-size", this.fontSize);
      // 创建分组
      let gs = g
        .selectAll(".circleText")
        .data(nodes)
        .enter()
        .append("g")
        .attr("transform", function (d) {
          let cirX = d.x;
          let cirY = d.y;
          return "translate(" + cirX + "," + cirY + ")";
        })
        .call(
          d3.drag().on("start", started).on("drag", dragged).on("end", ended)
        );
      // 绘制节点
      gs.append("circle")
        .attr("r", 10)
        .attr("fill", function (d, i) {
          return colorScale(i);
        });
      // 文字
      gs.append("text")
        .attr("x", -10)
        .attr("y", -20)
        .attr("dy", 10)
        .text(function (d) {
          return d.name;
        })
        .style("font-size", this.fontSize);
      // ticked
      function ticked() {
        glinks
          .attr("x1", function (d) {
            return d.source.x;
          })
          .attr("y1", function (d) {
            return d.source.y;
          })
          .attr("x2", function (d) {
            return d.target.x;
          })
          .attr("y2", function (d) {
            return d.target.y;
          });
        linksText
          .attr("x", function (d) {
            return (d.source.x + d.target.x) / 2;
          })
          .attr("y", function (d) {
            return (d.source.y + d.target.y) / 2;
          });
        gs.attr("transform", function (d) {
          return "translate(" + d.x + "," + d.y + ")";
        });
      }

      // 拖拽事件
      function started(event, d) {
        if (!event.active) {
          forceSimulation.alphaTarget(0.8).restart(); // 设置衰减系数，对节点位置移动过程的模拟，数值越高移动越快，数值范围[0, 1]
        }
        d.fx = d.x;
        d.fy = d.y;
      }
      function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
      }
      function ended(event, d) {
        if (!event.active) {
          forceSimulation.alphaTarget(0);
        }
        d.fx = null;
        d.fy = null;
      }
    },

    svgMouseover(e) {
      if (e.target.nodeName === "circle") {
        if (this.pinned.length === 0) {
          this.selectedState(e);
        }
        // 强制刷新
        this.$forceUpdate();
        this.$emit("hoverNode", e, e.target.__data__);
      }
    },

    svgMouseout(e) {
      if (e.target.nodeName === "circle") {
        
        this.noSelectedState(e);
        
        // 强制刷新
        this.$forceUpdate();
      }
    },

    selectedState(e) {
      // 节点自身显示文字、增加 selected class、添加进 selection
      // e.target.__data__.showText = true;
      e.target.classList.add("selected");
      console.log(e.target.__data__);
      this.selection.nodes.push(e.target.__data__);
      // 周围节点显示文字、边和结点增加 selected class、添加进 selection
      this.lightNeibor(e.target.__data__);
      // 除了 selected 的其余节点透明度减小
      console.log(d3.selectAll(".selected"));
      d3.selectAll(".element").style("opacity", 0.2);
    },

    noSelectedState(e) {
      // 节点自身不显示文字、移除 selected class
      // e.target.__data__.showText = false;
      e.target.classList.remove("selected");
      // 周围节点不显示文字、边和结点移除 selected class
      this.darkenNerbor();
      // 所有节点透明度恢复
      d3.selectAll(".element").style("opacity", 1);
    },

    pinnedState(e) {
      console.log(e.target);
      this.pinned.push(e.target.__data__.index);
      d3.selectAll(".element").style("opacity", 0.05);
    },

    lightNeibor(node) {
      this.links.forEach((link) => {
        console.log(link);
        if (link.source.index === node.index) {
          link.classList.add("selected");
          link.selected = "selected";
          this.selection.links.push(link);
          this.selection.nodes.push(link.target);
          this.lightNode(link.target);
        }
        if (link.target.index === node.index) {
          link.classList.add("selected");
          link.selected = "selected";
          this.selection.links.push(link);
          this.selection.nodes.push(link.source);
          this.lightNode(link.source);
        }
      });
    },

    lightNode(selectedNode) {
      this.nodes.forEach((node) => {
        if (node.index === selectedNode.index) {
          // node.showText = true;
        }
      });
    },

    darkenNerbor() {
      this.links.forEach((link) => {
        this.selection.links.forEach((selectedLink) => {
          if (selectedLink.id === link.id) {
            link.selected = "";
          }
        });
      });
      this.nodes.forEach((node) => {
        this.selection.nodes.forEach((selectednode) => {
          if (selectednode.id === node.id) {
            // node.showText = false;
          }
        });
      });
      // 清空 selection
      this.selection.nodes = [];
      this.selection.links = [];
    },

  },
};
</script>

<style scoped>
svg{

}
.element {
  transition: opacity 0.5s ease;
}
.selected {
  opacity: 1 !important;
}
.node,
.link {
  cursor: pointer;
}
</style>