<template>
    <div>
        <p class="text-success">{{ successText }}</p>
        <form v-on:submit.prevent="savePhoto" v-if="!many || images.length < max">
            <input type="file"
                   ref="file"
                   v-bind:name="uploadFieldName"
                   v-on:change="onFileChange($event.target.files)"
            >
            <img width="250" v-if="imageURL" :src="imageURL" alt="avatar">
            <p class="text-danger">{{ errorText }}</p>
            <b-button type="submit" variant="primary" :disabled="saveButtonDisabled()">Save</b-button>
        </form>
        <div v-else>
            <p>You can upload only {{max}} photos</p>
        </div>

    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "FileUpload.vue",
        data () {
            return {
                selected_file: null,
                errorText: null,
                successText: null,
                maxSize: 2048,
                imageURL: null
            }
        },
        props: [
            'uploadFieldName',
            'images',
            'max',
            'many'
        ],
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
                        return (this.errorText = 'Your file is too big! Please select an image under 2MB')
                    }
                    this.selected_file = imageFile;
                    this.imageURL = URL.createObjectURL(imageFile);
                }
            },
            saveButtonDisabled() {
                if (this.selected_file === null)
                    return true;
                return !!(this.many && this.images.length > this.max);

            },
            savePhoto() {
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
                            },
                            withCredentials: true
                        }
                    )
                        .then(response => {
                            if(response.status === 200)
                            {
                                this.$emit('ImageUploadSuccess');
                                this.successText =  "Image uploaded!";
                                this.$notify({group: 'foo', type: 'success', title: 'Success', text: 'Image is uploaded!', duration: -1});
                            }
                        })
                        .catch(() => {
                            this.$notify({group: 'foo', type: 'error', title: 'Fail', text: 'There is an error', duration: -1});
                        }).finally(() => {
                            this.selected_file = null;
                            this.imageURL = null;
                    })
                }
            }
        }
    }
</script>

<style scoped>

</style>
