import type { UploadResponse } from '~/types/api'

const API_BASE = 'http://127.0.0.1:8000/v1/files';

export function useFiles() {
    const files = ref<string[]>([]);
    const loading = ref(false);
    const uploading = ref(false);
    const error = ref<string | null>(null);

    async function list() {
        loading.value = true;
        error.value = null;

        try {
            files.value = await $fetch<string[]>(`${API_BASE}/`);
        } catch {
            error.value = 'Failed to fetch files';
        } finally {
            loading.value = false;
        }
    }

    // Upload file on the server
    async function upload(file: File) {
        uploading.value = true;
        error.value = null;
        try {
            // FormData default way to send file using POST request
            const form = new FormData();
            form.append('file', file);
            await $fetch<UploadResponse>(`${API_BASE}/upload`, { method: 'POST', body: form });
            await list(); // refresh the list of files after upload
        } catch {
            error.value = 'Failed to upload file';
        } finally {
            uploading.value = false;
        }
    }

    async function download(key: string) {
        const blob = await $fetch<Blob>(`${API_BASE}/${encodeURIComponent(key)}`, { responseType: 'blob' });

        // temprorary link to download the file
        const url = URL.createObjectURL(blob);

        // create a temporary anchor element to trigger the download
        const link = document.createElement('a');
        link.href = url;
        link.download = key;
        document.body.appendChild(link);
        link.click();

        // Clean up the temporary link (clean up memory)
        document.body.removeChild(link);
        URL.revokeObjectURL(url);

    }

    // Delete file on the server
    async function remove(key: string) {
        files.value = files.value.filter((filename) => filename !== key);
        await $fetch(`${API_BASE}/${encodeURIComponent(key)}`, { method: 'DELETE' })
    }

    return { files, loading, uploading, error, list, upload, remove, download }
}