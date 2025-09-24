function Campaigns() {
  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Campaigns</h1>
        <p className="text-gray-600">Organize outreach campaigns and track notes</p>
      </div>

      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-medium text-gray-900">All Campaigns</h2>
            <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium">
              New Campaign
            </button>
          </div>
        </div>
        <div className="p-6">
          <p className="text-gray-500">Campaigns and notes management will be implemented here.</p>
        </div>
      </div>
    </div>
  );
}

export default Campaigns;