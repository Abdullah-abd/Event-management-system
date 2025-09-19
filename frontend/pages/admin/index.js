"use client";
import { useEffect, useState } from "react";
import AddEventModal from "../../components/AddEvent/AddEventModal";
import EditEventModal from "../../components/EditEventModal/EditEventModal";
import EventCard from "../../components/EventCard/EventCard";
import { deleteEvent, getEvents } from "../../utils/api"; // ✅ only fetch + delete here

const AdminEvents = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isAddOpen, setIsAddOpen] = useState(false);
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");

  // Fetch events on mount
  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    setLoading(true);
    try {
      const data = await getEvents();
      setEvents(data);
    } catch (err) {
      console.error("Error fetching events:", err);
    } finally {
      setLoading(false);
    }
  };

  // Filtered events based on search
  const filteredEvents = events.filter((event) =>
    (event.title || event.name)
      .toLowerCase()
      .includes(searchQuery.toLowerCase())
  );

  // Handle Add Event → just update state
  const handleSaveAdd = (newEvent) => {
    setEvents((prev) => [...prev, newEvent]);
    setIsAddOpen(false);
  };

  // Handle Edit Event → just update state
  const handleSaveEdit = (updatedEvent) => {
    setEvents((prev) =>
      prev.map((e) => (e.id === updatedEvent.id ? updatedEvent : e))
    );
    setIsEditOpen(false);
    setSelectedEvent(null);
  };

  const handleDelete = async (id) => {
    try {
      await deleteEvent(id);
      setEvents((prev) => prev.filter((e) => e.id !== id));
    } catch (err) {
      console.error("Error deleting event:", err);
    }
  };

  const openEditModal = (event) => {
    setSelectedEvent(event);
    setIsEditOpen(true);
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">
        Admin Portal - Events
      </h2>

      {/* Search & Add New */}
      <div className="flex items-center gap-4 mb-6">
        <input
          type="text"
          placeholder="Search by title..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
        />
        <button
          onClick={() => setIsAddOpen(true)}
          className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition"
        >
          + Add Event
        </button>
      </div>

      {/* Event Cards */}
      {loading ? (
        <p>Loading events...</p>
      ) : filteredEvents.length === 0 ? (
        <p>No events found.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredEvents.map((event) => (
            <EventCard
              key={event.id}
              event={event}
              onEdit={() => openEditModal(event)}
              onDelete={() => handleDelete(event.id)}
            />
          ))}
        </div>
      )}

      {/* Modals */}
      <AddEventModal
        isOpen={isAddOpen}
        onClose={() => setIsAddOpen(false)}
        onSave={handleSaveAdd}
      />

      <EditEventModal
        isOpen={isEditOpen}
        onClose={() => setIsEditOpen(false)}
        onSave={handleSaveEdit}
        event={selectedEvent}
      />
    </div>
  );
};

export default AdminEvents;
