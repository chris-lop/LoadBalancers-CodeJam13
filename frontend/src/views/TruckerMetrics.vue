<template>
    
    <Toast position="bottom-center" group="bc" @close="onClose" class="items-center">
            <template #message="slotProps" class="items-center">
                <div class="flex flex-column align-items-start" style="flex: 1">
                    <i class="pi pi-box self-center" style="font-size: 2rem; margin-right: 0.5rem;"></i>
                    <div class="font-medium text-lg my-3 text-900 pr-[10px]">{{ slotProps.message.summary }}</div>
                    <div>
                        <p>Price: {{ slotProps.message.data.profit }}</p>
                        <p>Distance: {{ slotProps.message.data.mileage }}</p>

                    </div>
                </div>
                <Button class="p-button-sm text-sm items-center px-2 py-1 self-center" severity="success" label="Accept" @click="onAccept()"></Button>
            </template>
        </Toast>
    
    <Container> 
        <div class="px-10 pt-16">
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
                        <DataTable :value="metrics.latestLoads" tableStyle="min-width: 30rem">
                            <template #header>
                                <div class="flex flex-wrap align-items-center justify-content-between gap-2">
                                    <span class="text-xl text-900 font-bold">Latest Loads</span>
                                    
                                </div>
                            </template>
                            <Column field="loadId" header="ID" sortable />
                            <Column field="profit" header="Profit" sortable />
                            <Column field="score" header="Score" sortable />
                            <Column field="timestamp" header="Time" sortable />
                        </DataTable>
                    </template>
                </Card>
                <Card class="col-span-1">
                    <template #content>
                        <MapboxMap
                        style="height: 400px"
                        :access-token=apiMapboxKey
                        map-style="mapbox://styles/mapbox/streets-v11"
                        :center="mapCenter"
                        :zoom="1" />
                    </template>
                </Card>
            </div>  
        </div>
    </Container>
</template>

<script>
import Container from "@/components/Container.vue";
import axios from 'axios';
import { MapboxMap } from '@studiometa/vue-mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
const baseUrl = import.meta.env.VITE_API_SERVER_URL;
const mapboxKey = import.meta.env.VITE_MAP_BOX_GL;

export default {
    name: "TruckerMetrics",
    props: ['username'],
    components: {
        Container,
        MapboxMap
    },
    data() {
        return {
            mapCenter : [0,0], 
            metrics: {},
            eventSource: null,
            apiMapboxKey: mapboxKey
        };
    },
    created() {
        this.getEvents()
        this.getMetrics()
        
    },
    mounted() {
        
    },
    methods: {
        async getMetrics() {
            try {
                const response = await axios.get(`${baseUrl}/metrics/${this.username}`)
                this.metrics = response.data
                // format
                this.metrics.mileage = this.metrics.mileage.toFixed(0)
                this.metrics.last_month_mileage = this.metrics.last_month_mileage.toFixed(0)
                
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
                    life: 12000,               
                });
                if(this.metrics.latestLoads.length >= 5) {
                    this.metrics.latestLoads.pop()
                }
                console.log(this.metrics.latestLoads)
                data.timestamp = data.timestamp.split('T')[1]
                this.metrics.latestLoads.unshift(data)
            };
            
            this.eventSource.onerror = (error) => {
                console.error('EventSource failed:', error);
            };
        },
        
        onClose() {
            console.log('onClose');
        },
        onAccept() {
            console.log('onAccept');
        },
        onDecline() {
            console.log('onDecline');
        },
    },   
};

</script>
