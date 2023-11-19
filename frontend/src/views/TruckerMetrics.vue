<template>
    <Toast position="bottom-center" group="bc" class="items-center">
            <template #message="slotProps" class="items-center">
                <div class="flex flex-column align-items-start" style="flex: 1">
                    <i class="pi pi-box self-center" style="font-size: 2rem; margin-right: 0.5rem;"></i>
                    <div class="font-medium text-lg my-3 text-900 pr-[10px]">{{ slotProps.message.summary }}</div>
                    <div>
                        <p>Price: {{ slotProps.message.data.profit }} $</p>
                        <p>Distance: {{ slotProps.message.data.mileage }} mi</p>

                    </div>
                </div>
                <Button class="p-button-sm text-sm items-center px-2 py-1 self-center" severity="success" label="Accept" @click="onAccept(slotProps.message.data.originLatitude,slotProps.message.data.originLongitude )"></Button>
            </template>
        </Toast>
    <Container> 
        <div class="px-10 pt-12 pb-4">
            <div class="grid grid-cols-4 gap-4 pb-4">
                <Card title="Metric 1" class="col-span-1">
                    <template #content>
                        <div class="flex justify-center pb-2">
                            <div class="flex flex-col items-center">
                                <div class="flex items-center">
                                    <i class="pi pi-money-bill" style="font-size: 1rem; margin-right: 0.5rem;"></i>
                                    <p class="text-gray-500">Earnings</p>
                                </div>
                                <p class="text-2xl">{{ metrics.earnings }} $</p>
                                <div class="flex flex-row justify-center">
                                    <div class="pr-1">
                                        <i class="pi" :class="{'pi-arrow-up': metrics.earnings - metrics.last_month_earnings >= 0, 'pi-arrow-down': metrics.earnings - metrics.last_month_earnings < 0}" :style="{'color': metrics.earnings - metrics.last_month_earnings >= 0 ? 'green' : 'red'}"></i>
                                    </div>
                                    <div>
                                        <p :style="{'color': metrics.earnings - metrics.last_month_earnings >= 0 ? 'green' : 'red'}">{{ metrics.earnings - metrics.last_month_earnings >= 0 ? '+' : '-' }}{{ Math.abs(metrics.earnings - metrics.last_month_earnings) }} $</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                </Card>
                <Card title="Metric 2" class="col-span-1">
                    <template #content>
                        <div class="flex justify-center pb-2">
                            <div class="flex flex-col items-center">
                                <div class="flex items-center">
                                    <i class="pi pi-truck" style="font-size: 1rem; margin-right: 0.5rem;"></i>
                                    <p class="text-gray-500">Mileage</p>
                                </div>
                                <p class="text-2xl">{{ metrics.mileage }} mi</p>
                                <div class="flex flex-row justify-center">
                                    <div class="pr-1">
                                        <i class="pi" :class="{'pi-arrow-up': metrics.mileage - metrics.last_month_mileage >= 0, 'pi-arrow-down': metrics.mileage - metrics.last_month_mileage < 0}" :style="{'color': metrics.mileage - metrics.last_month_mileage >= 0 ? 'green' : 'red'}"></i>
                                    </div>
                                    <div>
                                        <p :style="{'color': metrics.mileage - metrics.last_month_mileage >= 0 ? 'green' : 'red'}">{{metrics.mileage - metrics.last_month_mileage >= 0 ? '+' : '-'}}{{ Math.abs(metrics.mileage - metrics.last_month_mileage) }} mi</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                </Card>
                
                <Card title="Metric 3" class="col-span-1">
                    <template #content>
                        <div class="flex justify-center pb-2">
                            <div class="flex flex-col items-center">
                                <div class="flex items-center">
                                    <i class="pi pi-cog" style="font-size: 1rem; margin-right: 0.5rem;"></i>
                                    <p class="text-gray-500">Equipment Type</p>
                                </div>
                                <p class="text-2xl">{{ metrics.equipType }}</p>
                            </div>
                        </div>
                    </template>
                </Card>
                
                <Card title="Metric 4" class="col-span-1">
                    <template #content>
                        <div class="flex justify-center pb-2">
                            <div class="flex flex-col items-center">
                                <div class="flex items-center">
                                    <i class="pi pi-map-marker" style="font-size: 1rem; margin-right: 0.5rem;"></i>
                                    <p class="text-gray-500">Next Trip Length Preference</p>
                                </div>
                                <p class="text-2xl">{{ metrics.nextTripLengthPreference }}</p>
                            </div>
                        </div>
                    </template>
                </Card>
            </div>
            <div class="grid grid-cols-2 gap-4">
                <Card class="col-span-1">
                    <template #content>
                        <DataTable :value="metrics.latestLoads" v-model:selection="selectedLoad" @rowSelect="onRowSelect" selectionMode="single" tableStyle="min-width: 25rem">
                            <template #header>
                                <div class="flex flex-wrap align-items-center justify-content-between gap-2">
                                    <span class="text-xl text-900 font-bold">Latest Loads</span>
                                </div>
                            </template>
                            <Column field="loadId" header="ID" sortable />
                            <Column field="profit" header="Profit" sortable />
                            <Column field="mileage" header="Mileage" sortable />
                            <Column field="timestamp" header="Time" sortable />
                        </DataTable>
                    </template>
                </Card>
                <Card class="col-span-1">
                    <template #content>
                        <Map v-model="location"/>
                    </template>
                </Card>
            </div>  
        </div>
    </Container>
</template>

<script>
import Container from "@/components/Container.vue";
import axios from 'axios';
import { MapboxMap, MapboxMarker, MapboxGeolocateControl, MapboxGeocoder } from '@studiometa/vue-mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import '@mapbox/mapbox-gl-geocoder/lib/mapbox-gl-geocoder.css';
import Map from '../components/Map.vue';
import "../../node_modules/mapbox-gl/dist/mapbox-gl.css"
const baseUrl = import.meta.env.VITE_API_SERVER_URL;
const mapboxKey = import.meta.env.VITE_MAP_BOX_GL;

export default {
    name: "TruckerMetrics",
    props: ['username'],
    components: {
        Container,
        MapboxMap,
        MapboxMarker,
        MapboxGeolocateControl,
        MapboxGeocoder,
        Map
    },
    data() {
        return {
            mapCenter: [0, 0], 
            metrics: {},
            eventSource: null,
            apiMapboxKey: mapboxKey,
            selectedLoad: null,
            startingPin: [0, 0],
            destinationPin: [0, 0],
            control: null,
            location: {
                lng: 0,
                lat: 0,
                zoom: 1,
                bearing: 0,
                pitch: 0,
                secLng: 0,
                secLat: 0
            }
        };
    },
    async created() {
        this.getEvents()
        await this.getMetrics()
        this.location.secLat = this.location.lat
        this.location.secLng = this.location.lng
    },
    mounted() {

    },
    methods: {
        async getMetrics() {
            try {
                const response = await axios.get(`${baseUrl}/metrics/${this.username}`)
                this.metrics = response.data
                // format
                console.log(this.metrics)
                this.metrics.mileage = this.metrics.mileage.toFixed(0)
                this.metrics.last_month_mileage = this.metrics.last_month_mileage.toFixed(0)
                this.location.lng = this.metrics.positionLongitude
                this.location.lat = this.metrics.positionLatitude
                this.metrics.latestLoads.forEach(load => {
                    load.profit = load.profit.toFixed(2)
                    load.score = load.score.toFixed(2)
                    
                    // format timestamp to only show date
                    load.timestamp = load.timestamp.split('T')[1]
                });
            } catch (error) {
                console.log(error)
            }
        },
        getEvents() {
            const eventUrl = `${baseUrl}/events/${this.username}`;
            this.eventSource = new EventSource(eventUrl);
            
            this.eventSource.onmessage = (event) => {
                let data = JSON.parse(event.data);
                data.profit = data.profit.toFixed(2)
                data.score = data.score.toFixed(2)
                console.log(data);
                this.$toast.add({
                    severity: 'success',
                    summary: 'New Load',
                    group: 'bc', 
                    data: data,
                    life: 6000,               
                });
                if(this.metrics.latestLoads.length >= 5) {
                    this.metrics.latestLoads.pop()
                }
                data.timestamp = data.timestamp.split('T')[1]
                this.metrics.latestLoads.unshift(data)
            };
            
            this.eventSource.onerror = (error) => {
                console.error('EventSource failed:', error);
            };
        },
        onRowSelect(event) {
            this.location.secLat = event.data.originLatitude
            this.location.secLng = event.data.originLongitude
        },
        search(query){
            console.log(query)
            console.log(this.control)
            if (this.control){
                console.log(this.geocodeControl)
                this.control.query(query)
            }
        },
        onAccept(lat,lgt) {
            this.location.secLat = lat
            this.location.secLng = lgt
        },
    },   
};

</script>

<style scoped>

</style>