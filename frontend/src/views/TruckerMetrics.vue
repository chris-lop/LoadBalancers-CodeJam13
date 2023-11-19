<template>
    <Container>
        <div class="px-10 pt-16">
            <div class="grid grid-cols-4 gap-4 pb-4">
                <Card title="Metric 1" class="col-span-1">
                    <template #content>
                        <div class="flex flex-row justify-center pb-2">
                            <div class="pr-2">
                                <i class="pi pi-money-bill"></i>
                            </div>
                            <div>
                                <p>Earnings</p>
                            </div>
                        </div>
                        <div class="flex flex-row justify-center pb-2">
                            <p>{{ metrics.earnings }}$</p>
                        </div>
                        <div class="flex flex-row justify-center">
                            <div class="pr-1">
                                <i class="pi" :class="{'pi-arrow-up': metrics.earnings - metrics.last_month_earnings >= 0, 'pi-arrow-down': metrics.earnings - metrics.last_month_earnings < 0}"></i>
                            </div>
                            <div>
                                <p>{{ metrics.earnings - metrics.last_month_earnings }}$</p>
                            </div>
                        </div>
                    </template>
                </Card>
                <Card title="Metric 2" class="col-span-1">
                    <template #content>
                    <p>Mileage</p>
                    <p>{{ metrics.mileage }}</p>
                    <p>+25</p>
                    </template>
                </Card>
                <Card title="Metric 3" class="col-span-1">
                    <template #content>
                    <p>Equipment Type</p>
                    <p>{{ metrics.equipType}}</p>
                    </template>
                </Card>
                <Card title="Metric 4" class="col-span-1">
                    <template #content>
                    <p>Next Trip Length Preference</p>
                    <p>{{ metrics.nextTripLengthPreference }}</p>
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
                                    <Button icon="pi pi-refresh" rounded raised />
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
            try {

            } catch (error) {

            }
        }
    },        
};
</script>
