# Claude prompt — animated Rajasthan cricket landing

Integrate the provided animated hero into my existing SUPERR Intelligence landing page.

- Use `images/rajasthan-cricket-landing-loop.gif` as the full-bleed hero visual.
- Use `images/rajasthan-cricket-landing-hero.jpg` as poster and reduced-motion/mobile fallback.
- Overlay real HTML text, never bake text into the image.
- Headline: “The game changes under pressure.”
- Supporting line: “Where Rajasthan's royal spirit meets the science of cricket.”
- CTA: “Enter the scouting war room”.
- Keep the scene visible: camel mascot playing cricket, stadium crowd in colourful Rajasthani attire, Jaipur-inspired fort/palace, floodlights and sunset.
- Apply a dark left-side gradient to ensure strong contrast and keep the CTA highly visible.
- Use `object-fit: cover` and tune `object-position` per breakpoint to avoid cropping the mascot or palace.
- Respect `prefers-reduced-motion`; use the JPG poster for reduced motion.
- Keep page weight in mind: lazy-load below-the-fold images, preload the hero poster, and use the GIF only for the hero.
- Keep all navigation and CTA accessible and keyboard-operable.
- Deliver updated standalone HTML AND complete source ZIP.
