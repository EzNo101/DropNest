<script setup lang="ts">
const { files, loading, uploading, error, list, upload, remove, download } = useFiles();

// Fetch the list of files when the component is mounted
onMounted(async () =>{
    await list();
})

async function onUploaded(uploaded: File[]){
    for(const file of uploaded){
        await upload(file);
    }
}

async function onDelete(key: string){
    if (confirm(`Are you sure you want to delete ${key}?`)){
        await remove(key);
    }
}
</script>

<template>
    <main class="mx-auto max-w-5xl px-6 py-10">
        <h1 class="text-6xl font-extrabold tracking-tight">
            <span class="bg-linear-to-r from-accent to-teal-300 bg-clip-text text-transparent">DropNest</span>
        </h1>
        <p class="mt-2 text-slate-400">Your cloud storage</p>

        <!-- busy prop, uploaded emit event -->
        <FileDropZone :busy="uploading" @uploaded="onUploaded" />

        <p v-if="loading" class="mt-4 text-slate-400">Loading files...</p>
        <p v-else-if="error" class="mt-4 text-danger">Error: {{ error }} </p>
        <p v-else-if="!files.length" class="mt-10 text-center text-slate-500">
            No files uploaded yet. Drop a file above or choose a file to get started.
        </p>

        <FileList :files="files" @download="download" @delete="onDelete" />
    </main>
</template>