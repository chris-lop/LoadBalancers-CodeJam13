<template>
    <div class="flex flex-col min-h-screen bg-slate-200">
        <div class="pt-36">
            <slot></slot>
        </div>
    </div>
</template>

<script>
export default {
    name: "Container",
    data() {
        return {};
    },
    methods: {}
};
</script>
