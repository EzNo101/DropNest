<script setup lang="ts">
const emit = defineEmits<{ uploaded: [files: File[]] }>();

defineProps<{ busy?: boolean }>();

// Hightlight the dropzone when a file is dragged over it
const dragActive = ref(false);

const input = ref<HTMLInputElement | null>(null);

function onDrop(event: DragEvent){
    dragActive.value = false;
    const dropped = event.dataTransfer?.files;
    if(dropped?.length){
        emit('uploaded', Array.from(dropped));
    }
}

// File choosen via dialog
function onPick(event: Event){
    const picked = (event.target as HTMLInputElement).files;
    if(picked?.length){
        emit('uploaded', Array.from(picked));
    }
    // Reset the input value so the same file can be picked again
    (event.target as HTMLInputElement).value = '';}
</script>

<template>
    <div
        class="mt-8 cursor-pointer rounded-2xl border-2 border-dashed bg-panel p-10 text-center transition-colors"
        :class="dragActive ? 'border-accent bg-accent/10' : 'border-line hover:border-accent-hover'"
        @click="input?.click()"
        @dragover.prevent="dragActive = true"
        @dragLeave="dragActive = false"
        @drop.prevent="onDrop"
    >
        <input ref="input" type="file" class="hidden" @change="onPick">

        <p class="text-lg font-medium text-slate-200">Drop file here</p>
        <p class="mt-1 text-sm text-slate-500">or click to browse</p>
    </div>
</template>