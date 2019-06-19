<template>
  <div id=leaflet-map>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.0.3/dist/leaflet.css" />
    <div id="map"></div>
  </div>
</template>

<script>
import L from "leaflet";
// import { EventBus } from "../main.js"

const MAP_CENTER_NO_LOCATION_AVAIL = [44.498955, 11.327591];  // Bologna
const ZOOM_LEVEL_NO_LOCATION_AVAIL = 7;
const ZOOM_LEVEL_FIRST_LOCATION = 14;

export default {
  data() {
    return {
      // map: null,
      // tileLayer: null,
      // firstLocationInfo: true
    }
  },
  methods: {
    // initMap() {
    //   let mapCenter;
    //   let zoomLevel;
    //   // if (this.located) {
    //   //   mapCenter = this.located;
    //   //   zoomLevel = ZOOM_LEVEL_FIRST_LOCATION
    //   //   this.firstLocationInfo = false;
    //   // } else {
    //   //   mapCenter = MAP_CENTER_NO_LOCATION_AVAIL;
    //   //   zoomLevel = ZOOM_LEVEL_NO_LOCATION_AVAIL;
    //   // }
    //   mapCenter = MAP_CENTER_NO_LOCATION_AVAIL;
    //   zoomLevel = ZOOM_LEVEL_NO_LOCATION_AVAIL;
      // this.myMap = L.map('map', {
      //   attributionControl: false,
      //   doubleClickZoom: false,
      // }).setView(mapCenter, zoomLevel);
    // },
    // initTileLayer() {
    //   this.tileLayer = L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}{r}.png', {
    //     minZoom: MIN_ZOOM_LEVEL,
    //     ext: 'png'
    //   }).addTo(this.map);
    // }
    // // initUserLocationMarker() {
    // //   this.userLocationMarker = L.marker(
    // //     [this.located.lat, this.located.lng],
    // //     { icon: this.logged ? PIN_LOGGED_IN_ICON : PIN_LOGGED_OUT_ICON }
    // //   )
    // //     .bindPopup(L.popup({ closeButton: false }).setContent("You are here"))
    // //     .addTo(this.myMap);
    // // }
  },
  mounted() {
    const map = L.map('map').setView([37.4501001, -121.9107704], 4)
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', { attribution: '© OpenStreetMap' }).addTo(map)
    this.myMap = map

    // this.initMap();
    // this.initTileLayer();

    // if (this.located) {
    //   this.firstLocationInfo = false;
    //   const currentLatLng = L.latLng(this.located.lat, this.located.lng);
      
    //   this.initUserLocationMarker();
    //   this.initCenterButton();
      
    //   this.myMap.flyTo(currentLatLng, ZOOM_LEVEL_FIRST_LOCATION);
    //   this.maskLayer.setData([currentLatLng]);  // array of coordinates
    //   this.userLocationMarker.setLatLng(currentLatLng);
    // }
    
    // // get stripped messages now
    // this.getStripped(this.myMap.getBounds().getSouthWest(), this.myMap.getBounds().getNorthEast());
    
    // // get stripped messages in the future with stripped polling
    // this.strippedPolling = setInterval(function() {
    //   this.getStripped(this.myMap.getBounds().getSouthWest(), this.myMap.getBounds().getNorthEast());
    // }.bind(this), STRIPPED_POLLING_INTERVAL);
  }
}
</script>


<style>
#map {
  width: 100%;
  height: 775px;
}
</style>
