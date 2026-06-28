/**
 * Demo app: spins up a MapView with one feature layer using the toolkit.
 *
 * Run with:  npm install @arcgis/core && npm run dev
 */
import { createMapView } from "../src/index";

createMapView({
  container: "viewDiv",
  basemap: "topo-vector",
  center: [-118.244, 34.052], // Los Angeles
  zoom: 10,
  layers: [
    {
      url: "https://services.arcgis.com/V6ZHFr6zdgNZuVG0/arcgis/rest/services/Landscape_Trees/FeatureServer/0",
      title: "Trees",
      outFields: ["*"],
      popup: {
        title: "{Common_Name}",
        fields: [
          { fieldName: "Common_Name", label: "Common name" },
          { fieldName: "Genus", label: "Genus" },
          { fieldName: "Height", label: "Height (ft)" },
        ],
      },
      marker: { color: [34, 139, 34], size: 6 },
    },
  ],
});
