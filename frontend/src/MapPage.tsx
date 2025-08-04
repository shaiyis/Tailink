import React, { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl"
import "maplibre-gl/dist/maplibre-gl.css"

// Enable proper rendering for Hebrew (RTL)
maplibregl.setRTLTextPlugin(
    "https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.2.3/mapbox-gl-rtl-text.js",
    null,
    true
);

export function DogMap() {

    const mapContainerRef = useRef(null);

    useEffect(() => {

        const map = new maplibregl.Map({
            container: mapContainerRef.current,
            style: `https://api.maptiler.com/maps/streets-v2/style.json?key=${import.meta.env.VITE_MAPTILER_KEY}`,
            center: [34.860, 32.195],
            zoom: 14,
        });
    
        if (!mapContainerRef.current) {
            console.error("Map container is null");
            return;
        }

        // Patch missing images with transparent 1x1 image
        map.on("styleimagemissing", (e) => {
        if (!map.hasImage(e.id)) {
            const canvas = document.createElement("canvas");
            canvas.width = canvas.height = 1;
            const ctx = canvas.getContext("2d");
            if (ctx) {
            const imageData = ctx.getImageData(0, 0, 1, 1);
            map.addImage(e.id, imageData, { pixelRatio: 1 });
            }
        }
        });

        // Remove layers with broken icon references
        map.on("style.load", () => {
            const layers = map.getStyle().layers;
            if (!layers) return;
            for (const layer of layers) {
            const icon = layer.layout?.["icon-image"];
            if (layer.type === "symbol" && typeof icon === "string" && icon.startsWith("office")) {
                try {
                map.removeLayer(layer.id);
                } catch (err) {
                console.warn(`Couldn't remove layer ${layer.id}:`, err);
                }
            }
            }
        });

        map.on("load", async () => {
            console.log("Map loaded");

            try {
                const [placesRes, availabilitiesRes, dogsRes] = await Promise.all([
                fetch("http://localhost:8000/api/place/places/"),
                fetch("http://localhost:8000/api/owner/owner-availability/"),
                fetch('http://localhost:8000/api/owner/dogs/')
            ]);

            const places = await placesRes.json(); // [{id, name, lat, lon...}]
            const availabilities = await availabilitiesRes.json(); // [{place_id, dog, ...}]
            const dogs = await dogsRes.json();

            console.log("Places:", places);
            console.log("Availabilities:", availabilities);
            console.log("Dogs:", dogs);

            // Create a map of dog name -> picture
            const dogPhotoMap = Object.fromEntries(
                dogs.map((dog: any) => [dog.name, dog.picture])
            );
            console.log("Dog photo map:", dogPhotoMap);

            const merged = places
            .filter((place: any) => place.latitude && place.longitude)
            .map((place: any) => ({
                ...place,
                availabilities: availabilities.filter(
                (a: any) => a.place_id == place.id
                ),
            }));
            
            console.log("Merged data:", merged);

            merged.forEach((place: any) => {
                place.availabilities.forEach((a: any) => {
                    const el = document.createElement("div");
                    el.style.width = "40px";
                    el.style.height = "40px";
                    el.style.borderRadius = "50%";
                    el.style.overflow = "hidden";
                    el.style.display = "flex";
                    el.style.alignItems = "center";
                    el.style.justifyContent = "center";
                    el.style.background = "blue"; // debugging only

                    const dogIcon = document.createElement("img");

                    dogIcon.src = dogPhotoMap[a.dog];
                    console.log("Dog icon URL:", dogIcon.src);
                    
                    dogIcon.style.width = "100%";
                    dogIcon.style.height = "100%";
                    dogIcon.style.borderRadius = "50%";
                    dogIcon.style.objectFit = "cover";
                    dogIcon.style.display = "block";
                    
                    // document.body.appendChild(dogIcon.cloneNode(true));

                    const description = `From: ${new Date(a.start_time).toLocaleString()}<br>To: ${new Date(a.end_time).toLocaleString()}`;
                    
                    dogIcon.onload = () => {
                        el.appendChild(dogIcon);
                        
                        new maplibregl.Marker(el)
                            .setLngLat([parseFloat(place.longitude), parseFloat(place.latitude)])
                            .setPopup(
                                new maplibregl.Popup({ offset: 25 }).setHTML(
                                `<strong>${a.dog}</strong><br>${description}<br>Owner: ${a.owner_username}<br>Place: ${a.place_name}`
                                )
                            )
                            .addTo(map);
                    };
                });
            });
            } catch (err) {
                console.error("Failed to load place or availability data", err);
            }
        });

        // Add navigation controls (zoom buttons)
        map.addControl(new maplibregl.NavigationControl(), 'top-right');

            return () => map.remove();
        }, []);

        return (
            <div style={{ height: "100vh", width: "100%" }}>
                <div
                ref={mapContainerRef}
                style={{ height: "70%", width: "50%" }}
                ></div>
            </div>
        );
}
