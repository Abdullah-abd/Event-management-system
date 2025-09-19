const EventCard = ({ event, onEdit, onDelete }) => {
  return (
    <div className="bg-white rounded-2xl shadow-md overflow-hidden hover:shadow-lg transition transform hover:-translate-y-1">
      {/* Event Image */}
      <img
        src={event.image_url || "/events.png"} // ✅ use image_url
        alt={event.title || event.name}
        className="w-full h-48 object-cover"
      />

      {/* Event Details */}
      <div className="p-4">
        <h3 className="text-xl font-bold text-gray-800">
          {event.title || event.name} {/* Show title if available */}
        </h3>
        <p className="text-sm text-gray-500 mb-1">
          {event.date} at {event.time}
        </p>
        <p className="text-gray-600 text-sm mb-4">{event.description}</p>

        {/* Actions */}
        <div className="flex gap-2">
          <button
            onClick={onEdit}
            className="flex-1 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
          >
            Edit
          </button>
          <button
            onClick={() => onDelete(event.id)}
            className="flex-1 bg-red-600 text-white py-2 rounded-lg hover:bg-red-700 transition"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
};

export default EventCard;
