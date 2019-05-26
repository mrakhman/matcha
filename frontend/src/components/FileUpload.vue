<template>
    <div>
        <form>
            <input type="file"
                   ref="file"
                   :name="uploadFieldName"
                   @change="onFileChange($event.target.name, $event.target.files)"
            >
            <img width="150" v-if="imageURL" :src="imageURL" alt="avatar">
            <p class="text-danger">{{ errorText }}</p>
            <b-button variant="primary">Save</b-button>
        </form>

    </div>
</template>

<script>
    export default {
        name: "FileUpload.vue",
        data () {
            return {
                errorDialog: null,
                errorText: '',
                uploadFieldName: 'file',
                maxSize: 1024,
                imageURL: null
            }
        },
        props: {
            value: Object
        },
        methods: {
            onFileChange(fieldName, file) {
                const {maxSize} = this;
                let imageFile = file[0];
                if (file.length > 0) {
                    let size = imageFile.size / maxSize / maxSize;
                    if (!imageFile.type.match('image.*')) {
                        // check whether the upload is an image
                        this.errorDialog = true;
                        this.errorText = 'Please choose an image file'
                    } else if (size > 1) {
                        // check whether the size is greater than the size limit
                        this.errorDialog = true;
                        this.errorText = 'Your file is too big! Please select an image under 1MB'
                    } else {
                        // Append file into FormData and turn file into image URL
                        let formData = new FormData();
                        let imageURL = URL.createObjectURL(imageFile);
                        this.imageURL = imageURL;
                        formData.append(fieldName, imageFile);
                        // Emit the FormData and image URL to the parent component
                        this.$emit('input', {formData, imageURL})
                    }
                }
            }
        }
    }
</script>

<style scoped>

</style>
