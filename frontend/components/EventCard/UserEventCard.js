const UserEventCard = ({ event }) => {
  return (
    <div className="bg-white rounded-2xl shadow-md overflow-hidden hover:shadow-lg transition transform hover:-translate-y-1">
      {/* Event Image */}
      <img
        src={event.image_url || "/events.png"} // fallback to public/events.png
        alt={event.title || event.name}
        className="w-full h-48 object-cover"
      />

      {/* Event Details */}
      <div className="p-4">
        <h3 className="text-xl font-bold text-gray-800">
          {event.title || event.name}
        </h3>
        <p className="text-sm text-gray-500 mb-1">
          {event.date} at {event.time}
        </p>
        <p className="text-gray-600 text-sm">{event.description}</p>
      </div>
    </div>
  );
};

export default UserEventCard;
