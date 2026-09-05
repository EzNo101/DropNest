<script setup lang="ts">
const emit = defineEmits<{ download: [key: string]; delete: [key: string] }>();
defineProps<{ files: string[] }>();
</script>

<template>
    <ul v-if="files.length" class="mt-6 overflow-hidden rounded-xl border-line bg-panel">
        <li
            v-for="(name, index) in files"
            :key="name"
            class="flex items-center justify-between gap-4 px-5 py-4"
            :clss="index !== 0 ? 'border-t border-line' : ''"
        >
            <span class="truncate font-medium"> {{ name }} </span>
            <div class="flex shrink-0 gap-2">
                <button
                    class="rounded-lg px-3 py-1.5 text-sm font-medium text-accent transition-colors hover:bg-accent/10"
                    @click="emit('download', name)"
                >
                    Download
                </button>
                <button
                    class="rounded-lg px-3 py-1.5 text-sm font-medium text-danger transition-colors hover:bg-danger/10"
                    @click="emit('delete', name)"
                >
                    Delete
                </button>
            </div>
        </li>
    </ul>
</template>