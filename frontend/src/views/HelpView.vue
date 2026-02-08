<script setup lang="ts">
</script>

<template>
    <div class="help-container">
        <h1>welcome to simple dash</h1>
        <p class="subtitle">Usability-focused email campaign analytics that helps you visualize and compare your
            marketing performance</p>

        <section class="help-section">
            <div class="value-props">
                <div class="value-prop">
                    <div class="icon">📊</div>
                    <h3>Instant Insights</h3>
                    <p>Upload your campaign reports and instantly see trends, metrics, and performance comparisons
                        across all your email campaigns.</p>
                </div>
                <div class="value-prop">
                    <div class="icon">🔒</div>
                    <h3>Privacy First</h3>
                    <p>Files are parsed on the server and immediately discarded. No campaign data is permanently stored
                        - everything lives in your browser's session storage only.</p>
                </div>
                <div class="value-prop">
                    <div class="icon">🚀</div>
                    <h3>No Setup Required</h3>
                    <p>No accounts, no tracking, no cookies. Just upload your CSV files and view your dashboard
                        instantly.</p>
                </div>
            </div>
        </section>

        <section class="help-section">
            <h2>How It Works</h2>

            <div class="step">
                <h3>Step 1: Upload Your Reports</h3>
                <p>Export your campaign reports as CSV files from your email marketing platform (MailChimp or
                    MailerLite Classic).</p>
            </div>

            <div class="step">
                <h3>Step 2: Automatic Parsing</h3>
                <p>Our parser automatically detects your platform and extracts key metrics like open rates, click
                    rates, bounces, and more.</p>
            </div>

            <div class="step">
                <h3>Step 3: View Your Dashboard</h3>
                <p>Explore individual campaign performance or view trends across all your campaigns with interactive
                    charts and visualizations.</p>
            </div>
        </section>

        <section class="help-section">
            <h2>Supported Platforms</h2>
            <div class="platforms-grid">
                <div class="platform-card">
                    <h3>MailChimp</h3>
                    <p>Export your campaign reports as CSV files from the MailChimp dashboard. Each CSV can
                        contain
                        multiple campaigns, and duplicate campaigns (based on unique ID) will be automatically
                        deduplicated using the most recent upload.</p>
                </div>
                <div class="platform-card">
                    <h3>MailerLite Classic</h3>
                    <p>Export campaign reports from MailerLite Classic in CSV format.</p>
                </div>
            </div>
            <p class="platforms-note">
                <em>More platforms coming soon!</em>
            </p>
        </section>

        <section class="help-section privacy-box">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                stroke-width="2" class="privacy-icon">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
            </svg>
            <div>
                <h2>Your Data Stays Private</h2>
                <ul>
                    <li><strong>No persistent storage:</strong> Your CSV files are sent to the server for parsing, but
                        are immediately discarded after processing. No campaign data is stored on the server.</li>
                    <li><strong>Local browser storage only:</strong> Parsed campaign data is returned to your browser
                        and stored temporarily in session storage.</li>
                    <li><strong>Cleared when you leave:</strong> All data is automatically cleared when you close the
                        tab or navigate away.</li>
                    <li><strong>No accounts or tracking:</strong> No sign-up required, no cookies, no tracking.</li>
                </ul>
            </div>
        </section>

        <section class="help-section">
            <h2>File Requirements</h2>
            <ul>
                <li><strong>Format:</strong> CSV files only</li>
                <li><strong>Maximum file size:</strong> 10MB per file</li>
                <li><strong>Maximum files:</strong> 12 files per upload</li>
                <li><strong>Platform detection:</strong> Automatic (MailChimp and MailerLite Classic formats
                    recognized)</li>
            </ul>
        </section>

        <section class="help-section">
            <h2>Tips for Best Results</h2>
            <ul>
                <li>Upload multiple campaigns to unlock trend analysis and the send-time heatmap</li>
                <li>Make sure your CSV files are exported directly from your email platform without
                    modifications
                </li>
                <li>Campaign data is sorted chronologically by send date for accurate trend visualization</li>
                <li>If some files fail to parse, successfully parsed campaigns will still be displayed with a
                    warning banner</li>
                <li>For MailChimp: Duplicate campaigns (same unique ID) across multiple files will be
                    automatically
                    deduplicated, keeping the version from the most recent upload</li>
            </ul>
        </section>

        <section class="help-section">
            <h2>FAQ</h2>

            <div class="faq-item">
                <h3>My file failed to upload</h3>
                <p>Make sure your file is a valid CSV file from MailChimp or MailerLite Classic, under 10MB in size, and
                    not modified or corrupted.</p>
            </div>

            <div class="faq-item">
                <h3>I don't see my data on the dashboard</h3>
                <p>This can happen if all uploaded files failed to parse (check for error messages), you're using a
                    private/incognito window with session storage disabled, or your browser doesn't support session
                    storage.</p>
            </div>

            <div class="faq-item">
                <h3>Can I export or save my dashboard?</h3>
                <p>Currently, Simple Dash doesn't offer export functionality. You can take screenshots of your dashboard
                    or re-upload your files anytime to view the data again.</p>
            </div>

            <div class="faq-item">
                <h3>How long is my data stored?</h3>
                <p>Your campaign data is only stored in your browser's session storage and is automatically cleared when
                    you close the tab or navigate away. The server does not retain any data after parsing.</p>
            </div>

            <div class="faq-item">
                <h3>What if I have campaigns from different platforms?</h3>
                <p>You can upload CSV files from multiple platforms in the same session. The parser will automatically
                    detect and handle each platform's format independently.</p>
            </div>
        </section>

        <section class="help-section disclaimer-section">
            <h2>Disclaimer</h2>
            <p class="disclaimer-text">
                Simple Dash is provided "as-is" without any warranties or guarantees of any kind, express or
                implied. The developers and maintainers are not responsible for any data loss, parsing errors,
                service interruptions, or any other issues that may arise from using this tool. Use at your own risk.
            </p>
            <p class="disclaimer-text">
                While your CSV files are sent to the server for parsing and immediately discarded afterward with no
                persistent storage, you are responsible for ensuring your use of this tool complies with all applicable
                data privacy laws and regulations in your jurisdiction. Always handle campaign data in accordance with
                your organization's privacy policies and applicable laws.
            </p>
            <p class="disclaimer-text">
                This tool is intended for legitimate analytics and campaign monitoring purposes. The developers
                assume no liability for how users choose to use Simple Dash or the decisions made based on the
                analytics provided.
            </p>
        </section>
    </div>
</template>

<style scoped>
.help-container {
    padding: var(--spacing-xl);
    max-width: 1000px;
    margin: 0 auto;
    min-height: calc(100vh - var(--top-bar-height));
}

.help-container h1 {
    font-size: 2.5rem;
    color: var(--color-text);
    margin-bottom: var(--spacing-sm);
    text-align: center;
}

.subtitle {
    text-align: center;
    font-size: 1.2rem;
    color: var(--color-text-light);
    margin-bottom: var(--spacing-xl);
}

.help-section {
    background: var(--color-bg-white);
    border-radius: var(--radius-lg);
    padding: var(--spacing-xl);
    margin-bottom: var(--spacing-lg);
    box-shadow: var(--shadow-md);
}

.help-section h2 {
    font-size: 1.8rem;
    margin: 0 0 var(--spacing-lg) 0;
    padding-bottom: var(--spacing-sm);
    color: var(--color-text);
}

.help-section h3 {
    font-size: 1.3rem;
    color: var(--color-text);
    margin: 0 0 0.75rem 0;
}

.help-section p {
    font-size: var(--spacing-md);
    line-height: 1.6;
    color: var(--color-text-light);
    margin-bottom: var(--spacing-md);
}

.help-section ul {
    margin: var(--spacing-sm) 0 0 var(--spacing-lg);
    color: var(--color-text-light);
    line-height: 1.8;
}

.help-section ul li {
    margin-bottom: var(--spacing-sm);
}

.value-props {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--spacing-lg);
}

.value-prop {
    text-align: center;
    padding: var(--spacing-md);
}

.value-prop .icon {
    font-size: 3rem;
    margin-bottom: var(--spacing-sm);
}

.value-prop h3 {
    font-size: 1.2rem;
    color: var(--color-text);
    margin: var(--spacing-sm) 0;
}

.value-prop p {
    font-size: 0.95rem;
    line-height: 1.6;
    color: var(--color-text-light);
    margin: 0;
}

.step {
    margin-bottom: var(--spacing-xl);
}

.step:last-child {
    margin-bottom: 0;
}

.platforms-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--spacing-lg);
    margin-bottom: var(--spacing-lg);
}

.platform-card {
    padding: var(--spacing-lg);
    background-color: var(--color-bg);
    border: 2px solid var(--color-border-dark);
    border-radius: var(--radius-lg);
}

.platform-card h3 {
    margin-bottom: var(--spacing-sm);
}

.platform-card p {
    margin: 0;
    font-size: 0.95rem;
    color: var(--color-text-light);
}

.platforms-note {
    text-align: center;
    color: var(--color-text-lighter);
    font-size: 0.9rem;
}

.privacy-box {
    display: flex;
    gap: var(--spacing-lg);
    background: var(--color-bg-info-gradient);
    border-left: 5px solid var(--color-info);
}

.privacy-icon {
    width: 48px;
    height: 48px;
    color: var(--color-info);
    flex-shrink: 0;
}

.privacy-box h3 {
    margin-bottom: var(--spacing-md);
}

.privacy-box ul {
    margin: 0;
    padding-left: var(--spacing-lg);
}

.privacy-box li {
    margin-bottom: var(--spacing-sm);
    line-height: 1.6;
}

.faq-item {
    margin-bottom: var(--spacing-lg);
}

.faq-item:last-child {
    margin-bottom: 0;
}

.faq-item h3 {
    font-size: 1.1rem;
    color: var(--color-text);
    margin: 0 0 var(--spacing-sm) 0;
}

.faq-item p {
    margin: 0;
    font-size: 0.95rem;
    line-height: 1.7;
    color: var(--color-text-light);
}

.disclaimer-section {
    border-left: 5px solid var(--color-text-light);
}

.disclaimer-text {
    font-size: 0.9rem;
    line-height: 1.7;
    color: var(--color-text-light);
    margin: 0 0 var(--spacing-md) 0;
}

.disclaimer-text:last-child {
    margin-bottom: 0;
}

@media (max-width: 768px) {
    .help-container {
        padding: var(--spacing-md);
    }

    .help-container h1 {
        font-size: 2rem;
    }

    .value-props,
    .platforms-grid {
        grid-template-columns: 1fr;
    }

    .privacy-box {
        flex-direction: column;
        align-items: center;
    }
}
</style>
