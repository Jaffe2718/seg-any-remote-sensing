<template>
  <div id="map" class="map"></div>
</template>

<script>
import {BingMaps, ImageStatic} from 'ol/source';
import { Tile as TileLayer } from 'ol/layer';
import Map from 'ol/Map';
import View from 'ol/View';
import {ZoomToExtent} from "ol/control";
import {Projection, transform} from "ol/proj";
import ImageLayer from "ol/layer/Image";
import Static from 'ol/source/ImageStatic';
import {getCenter} from "ol/extent";

export default {
  data() {
    return {
      map: null,
      viewer:null,

    };
  },
  mounted() {
    this.initMap();
  },
  methods: {
    initMap: function () {
      const extent = [100, 100, 500, 480];
      const projection = new Projection({
        code: 'xkcd-image',
        units: 'pixels',
        extent: extent,
      });
      const map = new Map({
        layers: [
          new ImageLayer({
            source: new Static({
              //attributions: '© <a href="https://xkcd.com/license.html">xkcd</a>',
              url: 'https://imgs.xkcd.com/comics/online_communities.png',
              projection: projection,
              imageExtent: extent,
            }),
          }),
        ],
        target: 'map',
        view: new View({
          projection: projection,
          center: getCenter(extent),
          zoom: 2,
          maxZoom: 8,
        }),
      });
    },
  },

};
</script>

<style scoped>
.map {
  height: 550px;
  width:550px;
  margin-left: 400px;
  border:1px solid #000;

}
</style>
