<template>
  <div class="app-container">
    <!-- Header -->
    <header class="header">
      <h1>My Notes</h1>
      <p class="subtitle">Organize your thoughts and ideas</p>
    </header>

    <!-- Search and Filter Bar -->
    <div class="search-filter-bar">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search notes..."
        @input="filterNotes"
      />
      <select v-model="selectedTag" @change="filterNotes">
        <option value="">All Tags</option>
        <option v-for="tag in uniqueTags" :key="tag" :value="tag">
          {{ tag }}
        </option>
      </select>
      <select v-model="sortBy" @change="filterNotes">
        <option value="title">Sort by Title</option>
        <option value="id">Sort by Date</option>
      </select>
      <select v-model="sortOrder" @change="filterNotes">
        <option value="asc">Ascending</option>
        <option value="desc">Descending</option>
      </select>
    </div>

    <!-- Create/Edit Note Form -->
    <div class="note-form">
      <h2>{{ isEditing ? "Edit Note" : "Create New Note" }}</h2>
      <form @submit.prevent="handleSubmitNote">
        <div class="form-group">
          <label>Title</label>
          <input
            v-model="noteForm.title"
            type="text"
            required
            placeholder="Enter note title"
          />
        </div>
        <div class="form-group">
          <label>Content</label>
          <textarea
            v-model="noteForm.content"
            rows="4"
            required
            placeholder="Enter note content"
          ></textarea>
        </div>
        <div class="form-buttons">
          <button type="submit" class="btn primary">
            {{ isEditing ? "Update Note" : "Create Note" }}
          </button>
          <button
            v-if="isEditing"
            type="button"
            @click="cancelEdit"
            class="btn secondary"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>

    <!-- Loading Spinner -->
    <div v-if="loading" class="loader">
      <div class="spinner"></div>
    </div>

    <!-- Notes Grid -->
    <div v-else-if="filteredNotes.length" class="notes-grid">
      <div v-for="note in paginatedNotes" :key="note.id" class="note-card">
        <div class="note-header">
          <h3>{{ note.title }}</h3>
          <div class="note-actions">
            <button @click="editNote(note)" class="icon-btn edit">
              <i class="bi bi-pencil"></i>
            </button>
            <button @click="deleteNote(note.id)" class="icon-btn delete">
              <i class="bi bi-trash"></i>
            </button>
          </div>
        </div>
        <p class="note-content">{{ note.content }}</p>

        <!-- Tags -->
        <div class="tags-section">
          <div class="tags-list">
            <span v-for="(tag, index) in note.tags" :key="index" class="tag">
              {{ tag }}
              <button @click="deleteNoteTag(note.id, tag)" class="tag-remove">
                ×
              </button>
            </span>
          </div>
          <form @submit.prevent="addTag(note.id)" class="add-tag-form">
            <input
              v-model="tagForms[note.id]"
              type="text"
              placeholder="Add a tag"
            />
            <button type="submit" class="btn primary">Add</button>
          </form>
        </div>
      </div>
    </div>

    <!-- No Results Message -->
    <div v-else class="no-results">
      <h3>No notes found</h3>
    </div>

    <!-- Pagination -->
    <div v-if="filteredNotes.length > itemsPerPage" class="pagination">
      <button
        v-for="page in totalPages"
        :key="page"
        @click="currentPage = page"
        :class="['page-btn', { active: currentPage === page }]"
      >
        {{ page }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, computed } from "vue";
import axios from "axios";
const BASE_URL = import.meta.env.VITE_BASE_URL;
const notes = ref([]);
const isEditing = ref(false);

const loading = ref(false);
const tagForms = reactive({});
const searchQuery = ref("");
const selectedTag = ref("");
const sortBy = ref("title");
const sortOrder = ref("asc");
const currentPage = ref(1);
const itemsPerPage = 6;

const noteForm = reactive({
  title: "",
  content: "",
  user_id: 1, // Replace with actual user ID management
});
const uniqueTags = computed(() => {
  const tags = new Set();
  notes.value.forEach((note) => {
    note.tags.forEach((tag) => tags.add(tag));
  });
  return Array.from(tags);
});

const filteredNotes = computed(() => {
  let filtered = [...notes.value];

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      (note) =>
        note.title.toLowerCase().includes(query) ||
        note.content.toLowerCase().includes(query)
    );
  }

  // Tag filter
  if (selectedTag.value) {
    filtered = filtered.filter((note) => note.tags.includes(selectedTag.value));
  }

  // Sorting
  filtered.sort((a, b) => {
    const aVal = sortBy.value === "title" ? a.title : a.id;
    const bVal = sortBy.value === "title" ? b.title : b.id;

    if (sortOrder.value === "asc") {
      return aVal > bVal ? 1 : -1;
    } else {
      return aVal < bVal ? 1 : -1;
    }
  });

  return filtered;
});

const totalPages = computed(() =>
  Math.ceil(filteredNotes.value.length / itemsPerPage)
);

const paginatedNotes = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredNotes.value.slice(start, end);
});

// Fetch all notes
const fetchNotes = async () => {
  loading.value = true;
  try {
    const response = await axios.get(`${BASE_URL}/notes`);
    if (response.data.status === "success") {
      notes.value = response.data.data;
    }
  } catch (error) {
    console.error("Error fetching notes:", error);
    showAlert("Error fetching notes", "danger");
  } finally {
    loading.value = false;
  }
};

// Create/Update note
const handleSubmitNote = async () => {
  try {
    if (isEditing.value) {
      const response = await axios.put(
        `${BASE_URL}/notes/${noteForm.id}`,
        noteForm
      );
      if (response.data.status === "success") {
        await fetchNotes();
        resetForm();
        showAlert("Note updated successfully", "success");
      }
    } else {
      const response = await axios.post(`${BASE_URL}/notes`, noteForm);
      if (response.data.status === "success") {
        await fetchNotes();
        resetForm();
        showAlert("Note created successfully", "success");
      }
    }
  } catch (error) {
    console.error("Error saving note:", error);
    showAlert("Failed to save note", "danger");
  }
};

// Delete note
const deleteNote = async (noteId) => {
  if (!confirm("Are you sure you want to delete this note?")) return;
  try {
    await axios.delete(`${BASE_URL}/notes/${noteId}`);
    await fetchNotes();
    showAlert("Note deleted successfully", "success");
  } catch (error) {
    console.error("Error deleting note:", error);
    showAlert("Failed to delete note", "danger");
  }
};

// Edit note
const editNote = (note) => {
  noteForm.id = note.id;
  noteForm.title = note.title;
  noteForm.content = note.content;
  noteForm.user_id = note.user_id;
  isEditing.value = true;
  window.scrollTo({ top: 0, behavior: "smooth" });
};

// Cancel edit
const cancelEdit = () => {
  resetForm();
};

// Reset form
const resetForm = () => {
  noteForm.id = null;
  noteForm.title = "";
  noteForm.content = "";
  isEditing.value = false;
};
const deleteNoteTag = async (noteId, tagToDelete) => {
  try {
    const note = notes.value.find((n) => n.id === noteId);
    if (!note) return;

    await axios.delete(`${BASE_URL}notes/${noteId}/tags/${tagToDelete}`);
    await fetchNotes();
    showAlert("Tag deleted successfully", "success");
  } catch (error) {
    console.error("Error deleting tag:", error);
    showAlert("Failed to delete tag", "danger");
  }
};

// Filter notes
const filterNotes = () => {
  currentPage.value = 1; // Reset to first page when filtering
};

// Add tag
const addTag = async (noteId) => {
  if (!tagForms[noteId]) return;
  try {
    const response = await axios.post(`${BASE_URL}/tags`, {
      name: tagForms[noteId],
      note_id: noteId,
    });
    if (response.data.status === "success") {
      tagForms[noteId] = "";
      await fetchNotes();
      showAlert("Tag added successfully", "success");
    }
  } catch (error) {
    console.error("Error adding tag:", error);
    showAlert("Failed to add tag", "danger");
  }
};

// Delete tag
const deleteTag = async (noteId, tagName) => {
  try {
    // Find the tag ID from the note's tags
    const note = notes.value.find((n) => n.id === noteId);
    if (!note) return;

    const tagToDelete = note.tags.find((t) => t === tagName);
    if (!tagToDelete) return;

    await axios.delete(`${BASE_URL}/tags/${tagToDelete.id}`);
    await fetchNotes();
    showAlert("Tag deleted successfully", "success");
  } catch (error) {
    console.error("Error deleting tag:", error);
    showAlert("Failed to delete tag", "danger");
  }
};

// Show alert
const showAlert = (message, type) => {
  const alertDiv = document.createElement("div");
  alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
  alertDiv.style.zIndex = "1050";
  alertDiv.innerHTML = `
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
  document.body.appendChild(alertDiv);
  setTimeout(() => {
    alertDiv.remove();
  }, 3000);
};

// Load initial data
onMounted(() => {
  fetchNotes();
});
</script>
<style>
:root {
  --primary-color: #2c3e50;
  --secondary-color: #34495e;
  --accent-color: #ff0000;
  --background-color: #f5f6fa;
  --card-background: #ffffff;
  --card-border: var(--border-color);
  --text-color: #2c3e50;
  --border-color: #000000;
  --shadow: 0 2px 4px rgba(196, 169, 169, 0.1);
  --input-background: #f8f8f8; /* Light background for inputs */
  --input-text: #000000; /* Softer text color for inputs */
}

.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background: var(--background-color);
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 3rem;
}

.header h1 {
  font-size: 2.5rem;
  color: var(--primary-color);
  margin-bottom: 0.5rem;
}

.subtitle {
  color: var(--secondary-color);
  font-size: 1.1rem;
}

.search-filter-bar {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
  background: var(--card-background);
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: var(--shadow);
}

.search-filter-bar input,
.search-filter-bar select,
.form-group input,
.form-group textarea,
.add-tag-form input {
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 1rem;
  width: 100%;
  background-color: var(--input-background);
  color: var(--input-text);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.search-filter-bar input:focus,
.search-filter-bar select:focus,
.form-group input:focus,
.form-group textarea:focus,
.add-tag-form input:focus {
  outline: none;
  border-color: var(--accent-color);
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.1);
}

.note-form {
  background: var(--card-background);
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  box-shadow: var(--shadow);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--text-color);
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.btn.primary {
  background: var(--accent-color);
  color: white;
}

.btn.secondary {
  background: var(--secondary-color);
  color: white;
}

.notes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.note-card {
  background: var(--card-background);
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: var(--shadow);
  transition: transform 0.2s ease;
}

.note-card:hover {
  transform: translateY(-2px);
}

.note-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 1rem;
}

.note-header h3 {
  margin: 0;
  color: var(--text-color);
}

.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.icon-btn.edit {
  color: var(--accent-color);
}

.icon-btn.delete {
  color: #e74c3c;
}

.note-content {
  color: var(--text-color);
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.tags-section {
  border-top: 1px solid var(--border-color);
  padding-top: 1rem;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.tag {
  background: #f1f2f6;
  padding: 0.4rem 0.8rem;
  border-radius: 16px;
  font-size: 0.9rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.tag-remove {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  font-size: 1.2rem;
  color: var(--secondary-color);
}

.add-tag-form {
  display: flex;
  gap: 0.5rem;
}

.add-tag-form input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
}

.loader {
  display: flex;
  justify-content: center;
  padding: 2rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid var(--accent-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 2rem;
}

.page-btn {
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-color);
  background: var(--card-background);
  cursor: pointer;
  border-radius: 4px;
}

.page-btn.active {
  background: var(--accent-color);
  color: white;
  border-color: var(--accent-color);
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .app-container {
    padding: 1rem;
  }

  .notes-grid {
    grid-template-columns: 1fr;
  }

  .search-filter-bar {
    grid-template-columns: 1fr;
  }
}
</style>
