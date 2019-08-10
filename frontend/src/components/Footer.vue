<template>
    <div>
        <footer>
            <p class="footer_text"> Goodbye, world! </p>
        </footer>
    </div>
</template>

<script>
    export default {
        name: "Footer.vue"
    }
</script>

<style scoped>
    footer {
        flex-shrink: 0;
        background-color: dimgrey;
        color: white;
        text-align: center;
    }
    .footer_text {
        padding: 10px;
        margin: 0;
    }
</style>
