<template>
    <div>
        <pre class="mt-3 mb-0">{{ selected_file }}</pre>
        <form v-on:submit.prevent="savePhoto">
            <input type="file"
                   ref="file"
                   v-bind:name="uploadFieldName"
                   v-on:change="onFileChange($event.target.files)"
            >
            <img width="250" v-if="imageURL" :src="imageURL" alt="avatar">
            <p class="text-danger">{{ errorText }}</p>
            <b-button type="submit" variant="primary">Save</b-button>
        </form>

    </div>
</template>

<script>
    import  axios from 'axios';
    export default {
        name: "FileUpload.vue",
        data () {
            return {
                selected_file: null,
                errorText: null,
                uploadFieldName: 'image',
                maxSize: 2048,
                imageURL: null
            }
        },
        props: {
            value: Object
        },
        methods: {
            onFileChange(file) {
                console.log(file);
                console.log(file[0]);
                console.log(file[0].name);
                this.errorText = null;
                const {maxSize} = this;
                let imageFile = file[0];
                if (file.length > 0) {
                    let size = imageFile.size / maxSize / maxSize;
                    if (!imageFile.type.match('image.*')) {
                        // check whether the upload is an image
                        return (this.errorText = 'Please choose an image file')
                    }
                    if (size > 1) {
                        // check whether the size is greater than the size limit
                        return (this.errorText = 'Your file is too big! Please select an image under 1MB')
                    }
                    this.selected_file = imageFile;
                    let imageURL = URL.createObjectURL(imageFile);
                    this.imageURL = imageURL;
                }
            },
            savePhoto() {
                if (this.selected_file === null)
                    return(this.errorText = "Choose file");
                if (this.errorText != null)
                    return(this.errorText = "Can't save file, choose another");

                if (this.errorText === null) {
                    // Append file into FormData and turn file into image URL
                    const data = new FormData();
                    data.append(this.uploadFieldName, this.selected_file, this.selected_file.name);
                    console.log(data);

                    axios.post(this.$root.API_URL + '/images/upload', {
                        data
                    })
                        .then(response => {
                            // if(response.status === 200)
                            // {
                            //
                            // }
                            // TODO: console
                            console.log(response)
                        })
                        .catch(error => {
                            // if (error.response.status === 409) {
                            //     this.errors.user_exists = true;
                            // }
                            // TODO: console
                            console.log(error)
                        })
                }
            }
        }
    }
</script>

<style scoped>

</style>
