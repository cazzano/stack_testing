package com.example.myapplication;

import android.os.Bundle;
import android.view.View;
import android.widget.ImageButton;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import com.google.android.material.card.MaterialCardView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);

        // Apply window insets for edge-to-edge display
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        // Set up click listeners for buttons
        setupButtons();

        // Set up click listeners for cards
        setupCardClicks();
    }

    private void setupButtons() {
        // Settings button click
        ImageButton settingsButton = findViewById(R.id.settingsButton);
        if (settingsButton != null) {
            settingsButton.setOnClickListener(v -> {
                Toast.makeText(MainActivity.this, "Settings clicked", Toast.LENGTH_SHORT).show();
            });
        }

        // Dark mode toggle button click
        ImageButton darkModeButton = findViewById(R.id.darkModeButton);
        if (darkModeButton != null) {
            darkModeButton.setOnClickListener(v -> {
                Toast.makeText(MainActivity.this, "Dark mode toggle clicked", Toast.LENGTH_SHORT).show();
            });
        }
    }

    private void setupCardClicks() {
        // Set up click listeners for each language card
        setupCardClick(R.id.pythonCard, "Python");
        setupCardClick(R.id.javascriptCard, "JavaScript");
        setupCardClick(R.id.swiftCard, "Swift");
        setupCardClick(R.id.rustCard, "Rust");
        setupCardClick(R.id.kotlinCard, "Kotlin");
        setupCardClick(R.id.dartCard, "Dart");
        setupCardClick(R.id.goCard, "Go");
    }

    private void setupCardClick(int cardId, String language) {
        MaterialCardView card = findViewById(cardId);
        if (card != null) {
            card.setOnClickListener(v -> {
                Toast.makeText(MainActivity.this, language + " reference clicked", Toast.LENGTH_SHORT).show();
                // Navigate to the specific reference screen
                // Intent intent = new Intent(MainActivity.this, ReferenceActivity.class);
                // intent.putExtra("LANGUAGE", language);
                // startActivity(intent);
            });
        }
    }
}