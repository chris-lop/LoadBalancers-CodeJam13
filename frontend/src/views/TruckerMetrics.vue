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
                                <i class="pi pi-arrow-up"></i>
                            </div>
                            <div>
                                <p>+25</p>
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
                        <DataTable :value="latestLoads" tableStyle="min-width: 30rem">
                            <template #header>
                                <div class="flex flex-wrap align-items-center justify-content-between gap-2">
                                    <span class="text-xl text-900 font-bold">Latest Loads</span>
                                    <Button icon="pi pi-refresh" rounded raised />
                                </div>
                            </template>
                            <Column field="id" header="ID" sortable />
                            <Column field="code" header="Code" sortable />
                            <Column field="name" header="Name" sortable />
                            <Column field="description" header="Description" sortable />
                        </DataTable>
                    </template>
                </Card>
                <Card class="col-span-1">
                    <template #content>
                        
                    </template>
                </Card>
            </div>  
        </div>
    </Container>
</template>

<script>
import Container from "@/components/Container.vue";
import axios from 'axios'
const baseUrl = import.meta.env.VITE_API_SERVER_URL


export default {
    name: "TruckerMetrics",
    props: ['username'],
    components: {
        Container,
    },
    data() {
        return {
            metrics: {},
            latestLoads: [{
                id: '1000',
                code: 'f230fh0g3',
                name: 'Bamboo Watch',
                description: 'Product Description',
                image: 'bamboo-watch.jpg',
                price: 65,
                category: 'Accessories',
                quantity: 24,
                inventoryStatus: 'INSTOCK',
                rating: 5
            }],

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
                console.log(response)
                this.metrics = response.data
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
