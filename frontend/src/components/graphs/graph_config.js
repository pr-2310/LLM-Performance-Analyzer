import G6 from "@antv/g6"

const ICON_MAP = {
  normal: 'https://gw.alipayobjects.com/mdn/rms_8fd2eb/afts/img/A*0HC-SawWYUoAAAAAAAAAAABkARQnAQ',
  b: 'https://gw.alipayobjects.com/mdn/rms_8fd2eb/afts/img/A*sxK0RJ1UhNkAAAAAAAAAAABkARQnAQ',
};

G6.registerNode(
  'card-node',
  {
    drawShape: function drawShape(cfg, group) {
      const color = cfg.is_linear ? '#0070C0' : '#00B050'; // Changed colors to more professional tones
      const r = 2;
      const shape = group.addShape('rect', {
        attrs: {
          x: 0,
          y: 0,
          width: 150,
          height: 60,
          stroke: color,
          radius: r,
        },
        name: 'main-box',
        draggable: false, // Changed to false to make the graph static
      });

      group.addShape('rect', {
        attrs: {
          x: 0,
          y: 0,
          width: 150,
          height: 21,
          fill: color,
          radius: [r, r, 0, 0],
        },
        name: 'title-box',
        draggable: false, // Changed to false to make the graph static
      });

      group.addShape('image', {
        attrs: {
          x: 4,
          y: 2,
          height: 16,
          width: 16,
          cursor: 'pointer',
          img: ICON_MAP[cfg.nodeType || 'normal'],
        },
        name: 'node-icon',
      });

      group.addShape('text', {
        attrs: {
          textBaseline: 'top',
          y: 5,
          x: 24,
          lineHeight: 20,
          text: cfg.title,
          fill: '#fff',
        },
        name: 'title',
      });

      cfg.panels.forEach((item, index) => {
        group.addShape('text', {
          attrs: {
            textBaseline: 'top',
            y: 27,
            x: 24 + index * 60,
            lineHeight: 20,
            text: item.title,
            fill: 'rgba(0,0,0, 0.65)', // Darkened the text for better readability
          },
          name: `index-title-${index}`,
        });

        group.addShape('text', {
          attrs: {
            textBaseline: 'top',
            y: 45,
            x: 24 + index * 60,
            lineHeight: 20,
            text: item.value,
            fill: '#404040', // Changed to a darker grey for better contrast
          },
          name: `index-value-${index}`,
        });
      });
      return shape;
    },
  },
  'single-node',
);

export const graph_config = {
    container: 'graphContainer',
    width: window.innerWidth,
    height: window.innerHeight,
    defaultEdge: {
        type: 'polyline',
        sourceAnchor: 1,
        targetAnchor: 0,
        style: {
            endArrow: {
                path: G6.Arrow.triangle(5, 10),
                fill: "#888888", // Changed to a neutral grey
                opacity: 50,
            },
            stroke: "#333333", // Changed to a darker stroke for better visibility
        },
    },
    defaultNode: {
        type: 'modelRect',
        size: [190, 60],
        anchorPoints: [
            [0.5, 0],
            [0.5, 1]
        ],
        labelCfg:{
          offset: 15,
          style: {
            fill: '#000000',
            fontSize: 20,
            stroke: '#E7E7E7',
          }
        },
        descriptionCfg: {
          style: {
            fill: '#656565',
            fontSize: 14,
          },
        },
    },
    modes: {
        default: ['drag-canvas', 'lasso-select'],
    },
    layout: {
      type: 'dagre',
      nodesep: 10,
      ranksep: 20,
      controlPoints: true,
    },
}