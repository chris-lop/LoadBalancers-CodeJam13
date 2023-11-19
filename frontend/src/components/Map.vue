<template>
    <div ref="mapContainer" class="map-container"></div>
</template>

<script>
import mapboxgl from "mapbox-gl";
mapboxgl.accessToken = import.meta.env.VITE_MAP_BOX_GL;
export default {
    props: ['modelValue'],
    mounted() {
        const { lng, lat, zoom, bearing, pitch } = this.modelValue
        const map = new mapboxgl.Map({
            container: this.$refs.mapContainer,
            style: "mapbox://styles/mapbox/streets-v12", // Replace with your preferred map style
            center: [lng, lat],
            zoom: zoom,
        });
        console.log('mounted')
        console.log(this.modelValue)
        this.map = map;
    },
    unmounted() {
        this.map.remove();
        this.map = null;
    },
    
};
</script>

<style>
.map-container {
    flex: 1;
    width: 100%;
    height: 450px; /* Adjust as needed */
}
</style>