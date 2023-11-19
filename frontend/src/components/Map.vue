<template>
    <div ref="mapContainer" class="map-container"></div>
</template>

<script>
import mapboxgl from "mapbox-gl";
mapboxgl.accessToken = import.meta.env.VITE_MAP_BOX_GL;
export default {
    props: ['modelValue'],
    data() {
        return {
            firstMarker: null,
            secondMarker: null,
            map: null,
        };
    },
    watch: {
        modelValue: {
            handler(newValue) {
                
                const { lng, lat, zoom, secLat, secLng } = newValue;
                if (this.map) {
                    this.firstMarker.setLngLat([lng, lat]);
                    this.secondMarker.setLngLat([secLng, secLat]);
                    this.map.flyTo({
                        center: [secLng, secLat],
                        essential: true,
                        duration: 2000, // Duration in milliseconds
                        zoom: 6,
                    });
                }
            },
            deep: true,
        },
    },
    mounted() {
        const { lng, lat, zoom, bearing, pitch, secLng, secLat } = this.modelValue
        const map = new mapboxgl.Map({
            container: this.$refs.mapContainer,
            style: "mapbox://styles/mapbox/streets-v12", // Replace with your preferred map style
            center: [lng, lat],
            zoom: zoom,
        });
        this.firstMarker = new mapboxgl.Marker().setLngLat([lng, lat]).addTo(map);
        // second marker
        this.secondMarker = new mapboxgl.Marker({ color: 'red' })
        .setLngLat([secLng, secLat])
        .addTo(map);
        
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