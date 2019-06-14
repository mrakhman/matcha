<template>
    <div>
        <p class="text-success">{{ successText }}</p>
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
                successText: null,
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
                this.errorText = null;
                this.successText = null;
                const {maxSize} = this;
                let imageFile = file[0];
                if (file.length > 0) {
                    let size = imageFile.size / maxSize / maxSize;
                    if (!imageFile.type.match('image.*')) {
                        return (this.errorText = 'Please choose an image file')
                    }
                    if (size > 1) {
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
                    const data = new FormData();
                    data.append(this.uploadFieldName, this.selected_file, this.selected_file.name);

                    axios.post(this.$root.API_URL + '/images/upload',
                        data,
                        {
                            headers: {
                                'Content-Type': 'multipart/form-data'
                            }
                        }
                    )
                        .then(response => {
                            if(response.status === 200)
                            {
                                this.successText =  "Image uploaded!";
                                this.$notify({group: 'foo', type: 'success', title: 'Success', text: 'Image is uploaded!', duration: -1});
                            }
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
